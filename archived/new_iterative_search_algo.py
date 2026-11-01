from typing import Any


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        if not self.left and not self.right:
            self.children = tuple()
        elif self.left and not self.right:
            self.children = (left,)
        elif not self.left and self.right:
            self.children = (right,)
        else:
            self.children = (left, right,)


def single_stack_postorder_iterative_no_flags(root):
    def skip_siblings():
        while stack[-1] != marker:
            stack.pop()
        stack.pop()  # also removes the marker

    marker = 1  # marker is a node that is 'white'. If the ghost node is 'black', the marker will be removed by skip_siblings().
    stack = [root]

    while stack:
        node: Any = stack.pop()

        if node == marker or is_win(node.value):
            if stack:
                skip_siblings()
                if not stack:
                    return False
            continue

        elif node.children:
            stack.append(marker)
            for child in node.children:
                stack.append(child)

    return True


def single_stack_postorder_iterative_with_flags(root):
    def skip_siblings():
        if stack:
            while stack[-1] != marker:
                stack.pop()

    stack = [root]
    marker = 0  # marker is a node that tells the 'color' flag to invert
    color = 0  # 0 = black; 1 = white

    while stack:
        node: Any = stack.pop()

        if node == marker:
            color = not color
            if color:
                skip_siblings()
            continue

        if is_win(node.value):
            color = 1
            skip_siblings()
            continue

        elif node.children:
            stack.append(marker)
            for child in node.children:
                stack.append(child)

    return bool(color)


def is_win(val: int):
    if val in (4,6,):
        return True

    elif val in (5,7,):
        return False


# Example usage:
if __name__ == '__main__':
    # root1:
    #         1
    #       /   \
    #      2     3
    #     / \   / \
    #    4   5 6   7
    root1 = Node(1,
                 Node(2, Node(4), Node(5)),
                 Node(3, Node(6), Node(7))
                 )

    # root2:
    #         1
    #       /   \
    #      2     3
    root2 = Node(1,
                 Node(2),
                 Node(3)
                 )

    print(single_stack_postorder_iterative_no_flags(root1))
    # print(single_stack_postorder_iterative_with_flags(root1))