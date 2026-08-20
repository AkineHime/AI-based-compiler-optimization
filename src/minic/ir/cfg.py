from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass, field
from .tac import Opcode, TACInstruction, TACFunction, Label


@dataclass
class BasicBlock:
    id: int
    label: Optional[str] = None
    instructions: List[TACInstruction] = field(default_factory=list)
    predecessors: List['BasicBlock'] = field(default_factory=list)
    successors: List['BasicBlock'] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BasicBlock):
            return False
        return self.id == other.id

    def __repr__(self) -> str:
        return f"BB{self.id}(label={self.label}, insts={len(self.instructions)})"


@dataclass
class Loop:
    header: BasicBlock
    back_edge: Tuple[BasicBlock, BasicBlock]  # (latch, header)
    blocks: Set[BasicBlock]                   # All blocks belonging to this natural loop
    depth: int = 1


@dataclass
class CFG:
    entry: Optional[BasicBlock] = None
    blocks: List[BasicBlock] = field(default_factory=list)
    dominators: Dict[int, Set[int]] = field(default_factory=dict)       # bb_id -> set of dominator bb_ids
    idom: Dict[int, Optional[int]] = field(default_factory=dict)         # bb_id -> immediate dominator bb_id
    loops: List[Loop] = field(default_factory=list)

    def get_block_by_id(self, bb_id: int) -> Optional[BasicBlock]:
        for b in self.blocks:
            if b.id == bb_id:
                return b
        return None

    def get_max_loop_depth(self) -> int:
        if not self.loops:
            return 0
        return max(loop.depth for loop in self.loops)


def build_cfg_for_function(func: TACFunction) -> CFG:
    """Construct Control Flow Graph, Dominator sets, and Natural Loops for a TACFunction."""
    insts = func.instructions
    if not insts:
        return CFG()

    # Step 1: Identify leaders
    # Leaders are:
    # 1. First instruction
    # 2. Target of any jump/branch (a LABEL)
    # 3. Instruction immediately following any jump/branch/return
    is_leader = [False] * len(insts)
    is_leader[0] = True

    label_to_index: Dict[str, int] = {}
    for i, inst in enumerate(insts):
        if inst.opcode == Opcode.LABEL and inst.dst is not None:
            label_name = str(inst.dst)
            label_to_index[label_name] = i

    for i, inst in enumerate(insts):
        if inst.opcode in (Opcode.JUMP, Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE):
            target_label = str(inst.dst)
            if target_label in label_to_index:
                is_leader[label_to_index[target_label]] = True
            if i + 1 < len(insts):
                is_leader[i + 1] = True
        elif inst.opcode == Opcode.RETURN:
            if i + 1 < len(insts):
                is_leader[i + 1] = True
        elif inst.opcode == Opcode.LABEL:
            is_leader[i] = True

    # Step 2: Partition instructions into basic blocks
    blocks: List[BasicBlock] = []
    current_block: Optional[BasicBlock] = None
    block_id_counter = 0

    for i, inst in enumerate(insts):
        if is_leader[i]:
            if current_block is not None and current_block.instructions:
                blocks.append(current_block)
            label_str = str(inst.dst) if inst.opcode == Opcode.LABEL else None
            current_block = BasicBlock(id=block_id_counter, label=label_str)
            block_id_counter += 1

        if current_block is not None:
            current_block.instructions.append(inst)

    if current_block is not None and current_block.instructions:
        blocks.append(current_block)

    if not blocks:
        return CFG()

    # Map label names to BasicBlocks
    label_to_block: Dict[str, BasicBlock] = {}
    for b in blocks:
        if b.instructions and b.instructions[0].opcode == Opcode.LABEL:
            lbl = str(b.instructions[0].dst)
            label_to_block[lbl] = b

    # Step 3: Add CFG edges
    for i, b in enumerate(blocks):
        if not b.instructions:
            continue
        last_inst = b.instructions[-1]

        if last_inst.opcode == Opcode.JUMP:
            target = str(last_inst.dst)
            if target in label_to_block:
                succ = label_to_block[target]
                b.successors.append(succ)
                succ.predecessors.append(b)

        elif last_inst.opcode in (Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE):
            # Branch target
            target = str(last_inst.dst)
            if target in label_to_block:
                succ = label_to_block[target]
                b.successors.append(succ)
                succ.predecessors.append(b)
            # Fall-through
            if i + 1 < len(blocks):
                fallthrough = blocks[i + 1]
                b.successors.append(fallthrough)
                fallthrough.predecessors.append(b)

        elif last_inst.opcode == Opcode.RETURN:
            # Function exit block (no successors)
            pass

        else:
            # Normal fall-through
            if i + 1 < len(blocks):
                fallthrough = blocks[i + 1]
                b.successors.append(fallthrough)
                fallthrough.predecessors.append(b)

    cfg = CFG(entry=blocks[0], blocks=blocks)

    # Step 4: Compute Dominators using iterative dataflow
    _compute_dominators(cfg)

    # Step 5: Detect Natural Loops
    _detect_loops(cfg)

    return cfg


def _compute_dominators(cfg: CFG) -> None:
    """Compute dominator sets for all blocks in CFG."""
    if not cfg.blocks:
        return

    all_block_ids = {b.id for b in cfg.blocks}
    entry_id = cfg.entry.id if cfg.entry else cfg.blocks[0].id

    dom: Dict[int, Set[int]] = {}
    for b in cfg.blocks:
        if b.id == entry_id:
            dom[b.id] = {entry_id}
        else:
            dom[b.id] = set(all_block_ids)

    changed = True
    while changed:
        changed = False
        for b in cfg.blocks:
            if b.id == entry_id:
                continue

            if b.predecessors:
                pred_doms = [dom[p.id] for p in b.predecessors]
                intersected = set.intersection(*pred_doms) if pred_doms else set()
            else:
                intersected = set()

            new_dom = {b.id} | intersected
            if new_dom != dom[b.id]:
                dom[b.id] = new_dom
                changed = True

    cfg.dominators = dom

    # Compute immediate dominators (idom)
    idom: Dict[int, Optional[int]] = {}
    for b in cfg.blocks:
        if b.id == entry_id:
            idom[b.id] = None
            continue

        strict_doms = dom[b.id] - {b.id}
        curr_idom = None
        for d in strict_doms:
            # d is idom if it does not strictly dominate any other strict dominator
            is_immediate = True
            for other in strict_doms:
                if other != d and other in dom[d]:
                    is_immediate = False
                    break
            if is_immediate:
                curr_idom = d
                break
        idom[b.id] = curr_idom

    cfg.idom = idom


def _detect_loops(cfg: CFG) -> None:
    """Find back-edges and construct natural loops."""
    loops: List[Loop] = []

    for b in cfg.blocks:
        for succ in b.successors:
            # Back-edge check: succ dominates b
            if succ.id in cfg.dominators.get(b.id, set()):
                # succ is the loop header, b is the latch
                loop_blocks = _find_natural_loop_blocks(cfg, succ, b)
                loops.append(Loop(header=succ, back_edge=(b, succ), blocks=loop_blocks))

    # Calculate loop nesting depths
    for i, loop1 in enumerate(loops):
        depth = 1
        for j, loop2 in enumerate(loops):
            if i != j and loop1.blocks.issubset(loop2.blocks):
                depth += 1
        loop1.depth = depth

    cfg.loops = loops


def _find_natural_loop_blocks(cfg: CFG, header: BasicBlock, latch: BasicBlock) -> Set[BasicBlock]:
    """Given header and latch of a back-edge, collect all blocks in the natural loop."""
    loop_blocks: Set[BasicBlock] = {header}
    stack: List[BasicBlock] = []

    if latch != header:
        loop_blocks.add(latch)
        stack.append(latch)

    while stack:
        m = stack.pop()
        for p in m.predecessors:
            if p not in loop_blocks:
                loop_blocks.add(p)
                stack.append(p)

    return loop_blocks
