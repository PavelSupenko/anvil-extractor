from model.files.tree.file_data import FileData


class FileTree:
    def __init__(self, root_name: str, root_file_id: int):
        self.root = FileData(root_name, depth=1, file_id=root_file_id)

    def add_child(self, parent_name, child_name, file_id):
        parent = self._find_node(self.root, parent_name)
        if parent:
            child = FileData(child_name, depth=parent.depth + 1, file_id=file_id)
            parent.children.append(child)
            return True
        return False

    def remove_child(self, parent_name, child_name):
        parent = self._find_node(self.root, parent_name)
        if parent:
            for child in parent.children:
                if child.name == child_name:
                    parent.children.remove(child)
                    return True
        return False

    def get_sorted_tree(self):
        sorted_tree = []
        self._traverse_and_sort(self.root, sorted_tree)
        return sorted_tree

    def get_filtered_tree(self, filter_text):
        filtered_tree = []
        self._traverse_and_filter(self.root, filtered_tree, filter_text)
        return filtered_tree

    def find_file_by_name(self, name) -> FileData:
        return self._find_file_by_name(self.root, name)

    def find_file_by_name_and_parent(self, parent_name, file_name):
        matching_parents = [node for node in self.root.children if node.name == parent_name]
        for parent in matching_parents:
            for child in parent.children:
                if child.name == file_name:
                    return child
        return None

    def _find_file_by_name(self, current_node, name):
        if current_node.name == name:
            return current_node
        for child in current_node.children:
            result = self._find_file_by_name(child, name)
            if result:
                return result
        return None

    def _traverse_and_sort(self, node, sorted_tree):
        sorted_tree.append((node.name, node.depth))
        node.children.sort(key=lambda x: x.name)
        for child in node.children:
            self._traverse_and_sort(child, sorted_tree)

    def _traverse_and_filter(self, node, filtered_tree, filter_text):
        if filter_text in node.name:
            filtered_tree.append((node.name, node.depth))
        for child in node.children:
            self._traverse_and_filter(child, filtered_tree, filter_text)

    def _find_node(self, current_node, name):
        if current_node.name == name:
            return current_node
        for child in current_node.children:
            result = self._find_node(child, name)
            if result:
                return result
        return None
