import math
import graphviz

class Node:

    def __init__(self, order):
        self.order = order
        self.keys = []
        self.parent = None

    def is_full(self):
        return len(self.keys) == self.order


class LeafNode(Node):

    def __init__(self, order):
        super().__init__(order)
        self.prev = None
        self.next = None
        self.values = []


class InternalNode(Node):

    def __init__(self, order):
        super().__init__(order)
        self.children = []


class BPTree:

    def __init__(self, order=3, dtype=int):
        self.root = LeafNode(order)
        self.order = order
        self.dtype = dtype


    def search(self, key):

        leaf = self._find_leaf(key)

        start = 0
        end = len(leaf.keys) - 1

        while start <= end:

            mid = (start + end) // 2

            if key > leaf.keys[mid]:
                start = mid + 1

            elif key == leaf.keys[mid]:
                return leaf.values[mid]

            else:
                end = mid - 1

        return None


    def _find_leaf(self, key):

        curr = self.root

        while isinstance(curr, InternalNode):

            i = 0

            while i < len(curr.keys) and key >= curr.keys[i]:
                i += 1

            curr = curr.children[i]

        return curr


    def insert(self, key, value):

        root = self.root

        if len(root.keys) == self.order - 1:

            new_root = InternalNode(self.order)

            new_root.children.append(self.root)

            self.root = new_root

            self._split_child(new_root, 0)

            self._insert_non_full(new_root, key, value)

        else:

            self._insert_non_full(root, key, value)


    def _insert_non_full(self, node, key, value):

        if isinstance(node, LeafNode):

            insert_idx = 0

            while insert_idx < len(node.keys) and key > node.keys[insert_idx]:
                insert_idx += 1

            node.keys.insert(insert_idx, key)
            node.values.insert(insert_idx, value)

        else:

            insert_idx = 0

            while insert_idx < len(node.keys) and key >= node.keys[insert_idx]:
                insert_idx += 1

            child = node.children[insert_idx]

            if len(child.keys) == self.order - 1:

                self._split_child(node, insert_idx)

                if key >= node.keys[insert_idx]:
                    insert_idx += 1

            self._insert_non_full(node.children[insert_idx], key, value)


    def _split_child(self, parent, index):

        child = parent.children[index]

        mid = len(child.keys) // 2

        promoted_key = child.keys[mid]

        if isinstance(child, LeafNode):

            new_child = LeafNode(self.order)

            new_child.keys = child.keys[mid:]
            new_child.values = child.values[mid:]

            child.keys = child.keys[:mid]
            child.values = child.values[:mid]

            new_child.next = child.next

            if child.next:
                child.next.prev = new_child

            child.next = new_child
            new_child.prev = child

        else:

            new_child = InternalNode(self.order)

            new_child.keys = child.keys[mid + 1:]
            new_child.children = child.children[mid + 1:]

            child.keys = child.keys[:mid]
            child.children = child.children[:mid + 1]

        parent.keys.insert(index, promoted_key)
        parent.children.insert(index + 1, new_child)
        
    def update(self, key, new_value):
        """
        Update value associated with an existing key.
        Return True if successful.
        """

        leaf = self._find_leaf(key)

        for i, k in enumerate(leaf.keys):

            if k == key:

                leaf.values[i] = new_value

                return True

        return False


    def range_query(self, start_key, end_key):

        leaf = self._find_leaf(start_key)

        results = []

        while leaf:

            for i, key in enumerate(leaf.keys):

                if key > end_key:
                    return results

                if key >= start_key:
                    results.append((key, leaf.values[i]))

            leaf = leaf.next

        return results


    def get_all(self):

        results = []

        node = self.root

        while isinstance(node, InternalNode):
            node = node.children[0]

        while node:

            for i in range(len(node.keys)):
                results.append((node.keys[i], node.values[i]))

            node = node.next

        return results


    def visualize_tree(self, filename="bptree_visualization"):

        dot = graphviz.Digraph(name="B+Tree", format="png")

        # Make tree taller
        dot.attr(rankdir="TB")

        # Control spacing so it doesn't stretch too wide
        dot.attr(nodesep="0.5")
        dot.attr(ranksep="0.75")

        if self.root:
            self._add_nodes(dot, self.root)
            self._add_edges(dot, self.root)

        dot.render(filename, cleanup=True)


    def _add_nodes(self, dot, node):

        if isinstance(node, LeafNode):

            # show key:value pairs
            label_items = []

            for i in range(len(node.keys)):
                key = node.keys[i]
                val = node.values[i]

                # shorten long values for readability
                val_str = str(val)
                if len(val_str) > 12:
                    val_str = val_str[:12] + "..."

                label_items.append(f"{key}:{val_str}")

            label = "\\n".join(label_items)

            dot.node(
                str(id(node)),
                label,
                shape="box",
                style="filled",
                fillcolor="lightgreen"
            )

        else:

            label = " | ".join(str(k) for k in node.keys)

            dot.node(
                str(id(node)),
                label,
                shape="box",
                style="filled",
                fillcolor="lightblue"
            )

            for child in node.children:
                self._add_nodes(dot, child)


    def _add_edges(self, dot, node):

        if isinstance(node, InternalNode):

            for child in node.children:

                dot.edge(str(id(node)), str(id(child)))

                self._add_edges(dot, child)

        elif isinstance(node, LeafNode):

            if node.next:

                dot.edge(
                    str(id(node)),
                    str(id(node.next)),
                    style="dashed",
                    color="gray",
                    constraint="false"
                )
                
    def delete(self, key):

        if not self.root:
            return False

        deleted = self._delete(self.root, key)

        if isinstance(self.root, InternalNode) and len(self.root.keys) == 0:
            self.root = self.root.children[0]

        return deleted


    def _delete(self, node, key):

        if isinstance(node, LeafNode):

            for i, k in enumerate(node.keys):

                if k == key:

                    node.keys.pop(i)
                    node.values.pop(i)

                    return True

            return False

        else:

            i = 0

            while i < len(node.keys) and key >= node.keys[i]:
                i += 1

            deleted = self._delete(node.children[i], key)

            min_keys = math.ceil(self.order / 2) - 1

            if len(node.children[i].keys) < min_keys:
                self._fill_child(node, i)

            return deleted


    def _fill_child(self, node, index):

        min_keys = math.ceil(self.order / 2) - 1

        if index > 0 and len(node.children[index - 1].keys) > min_keys:
            self._borrow_from_prev(node, index)

        elif index < len(node.children) - 1 and len(node.children[index + 1].keys) > min_keys:
            self._borrow_from_next(node, index)

        else:

            if index < len(node.children) - 1:
                self._merge(node, index)

            else:
                self._merge(node, index - 1)


    def _borrow_from_prev(self, node, index):

        child = node.children[index]
        sibling = node.children[index - 1]

        if isinstance(child, LeafNode):

            child.keys.insert(0, sibling.keys.pop())
            child.values.insert(0, sibling.values.pop())

            node.keys[index - 1] = child.keys[0]

        else:

            child.keys.insert(0, node.keys[index - 1])
            child.children.insert(0, sibling.children.pop())

            node.keys[index - 1] = sibling.keys.pop()


    def _borrow_from_next(self, node, index):

        child = node.children[index]
        sibling = node.children[index + 1]

        if isinstance(child, LeafNode):

            child.keys.append(sibling.keys.pop(0))
            child.values.append(sibling.values.pop(0))

            node.keys[index] = sibling.keys[0]

        else:

            child.keys.append(node.keys[index])
            child.children.append(sibling.children.pop(0))

            node.keys[index] = sibling.keys.pop(0)


    def _merge(self, node, index):

        left_child = node.children[index]
        right_child = node.children[index + 1]

        if isinstance(left_child, LeafNode):

            left_child.keys.extend(right_child.keys)
            left_child.values.extend(right_child.values)

            left_child.next = right_child.next

            if right_child.next:
                right_child.next.prev = left_child

        else:

            left_child.keys.append(node.keys[index])
            left_child.keys.extend(right_child.keys)
            left_child.children.extend(right_child.children)

        node.keys.pop(index)
        node.children.pop(index + 1)