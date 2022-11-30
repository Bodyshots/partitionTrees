from sage.all import Partitions
from typing import List

class GroupTree:
    def __init__(self, num: int, height=0) -> None:
        self.element = num
        self.height = height
        self.children = self.create_children()

    def create_children(self) -> List["PartitionTree"]:
        """
        Return the possible integer partitions for <self.element> 
        as a list of PartitionTrees
        """
        return [PartitionTree(partition, self.element, self.height + 1) 
                for partition in Partitions(self.element)[1:]]

    def __str__(self) -> str:
        string = "\t" * self.height + f"{self.element} ({len(self.children)} partition(s))\n"
        for partition in self.children:
            string += f"{str(partition)}"

        return string

    def get_partition_num(self) -> int:
        """
        Returns the number of partitions for <self.element>
        """
        return len(self.children) + 1

    def get_partitions(self) -> str:
        """
        Note: The number of partitions printed does not include the element itself
        nor is the element itself printed as a partition
        """
        string = f"{self.get_partition_num()} partition(s) for {self.element}:\n"
        string += f"\t{str([self.element])}\n"
        for partition in self.children:
            string += f"\t{str(partition.partition)}\n"
        return string

    def get_num_k_partitions(self, k: int) -> int:
        """
        Return the number of <k>-lengthed partitions for <self.element>
        """
        count = 0
        if k == 1: count = 1
        else:
            for partition in self.children: 
                if len(partition.partition) == k: count += 1

        return count

    def partition_triangle(self) -> str:
        """
        Let n be self.element.

        Return the string representation of an nxn triangle where:
        - Every ith row represents the number that is to be partitioned,
        where 1 <= i <= n 
        - Every kth column represents the number of k-lengthed
        integer partitions made out every i, where 1 <= k <= n

        Note: Very reminiscient of Pascal's Triangle. However, unlike
        Pascal's Triangle:
        - An integer partition triangle does not follow Pascal's Triangle's
        recurrence definition
        - Row and column numbers start at 1, not 0

        Observations:
        - The first column of the triangle always only has "1" entries
        - For every ith row, their ith entry is always 1
        - The 2nd column's ith entry can be determined, based on i's parity:
            - If i is odd, then the ith entry of the 2nd column will be
            i / 2
            - If i is even, then the ith entry of the 2nd column will be
            (i + 1) / 2
        - If i <= k - 1, then the ith entry will be 0 (ie. there is no
        such k-lengthed integer partition for the number i)
        """
        ## Right-angled triangle version
        string = ""
        for n in range(1, self.element + 1):
            string += "\n1"
            tree = GroupTree(n)
            for k in range(2, self.element + 1):
                count = tree.get_num_k_partitions(k)
                if count != 0: string += f" {count}"
        return f"{string}\n"

        # from os import get_terminal_size
        # term_width = get_terminal_size().columns
        # string = ""
        # for n in range(1, self.element + 1): # column
        #     string += "\n1"
        #     tree = GroupTree(n)
        #     for k in range(2, n + 1): # row
        #         count = tree.get_num_k_partitions(k)
        #         string += f" {count}"

        # centered_strs = [row.center(term_width) for row in string.split("\n")]
        # res_string = ""
        # for centered_str in centered_strs: res_string += centered_str + "\n"
        # return res_string

    def get_triangle_row(self, row_num: int) -> List[int]:
        """
        Prereq: 1 <= row_num <= self.element
        """
        row = []
        for n in range(1, row_num + 1):
            tree = GroupTree(n)
            row = [tree.get_num_k_partitions(k) for k in range(1, n + 1)]
        return row

    def triangle_row_sum(self, row_num: int) -> int:
        return sum(self.get_triangle_row(row_num))

    def get_triangle_col(self, col_num: int) -> List[int]:
        """
        Prereq: 1 <= col_num <= self.element
        """
        if col_num == 1: return [1 for _ in range(self.element)]
        col = []
        for n in range(col_num - 1, self.element + 1):
            tree = GroupTree(n)
            col.append(tree.get_num_k_partitions(col_num))
        return col

    def triangle_col_sum(self, col_num: int) -> int:
        return sum(self.get_triangle_col(col_num))

    def get_triangle_entry(self, col_num: int, row_num: int):
        """
        Return the number of <col_num>-lengthed partitions
        that can be made out of <row_num>.

        Recursively, one can compute the value of this same entry
        by returning:

        "# of (<col_num> - 1)-lengthed partitions for <row_num> - 1" + 
        "# of (<col_num>)-lengthed partitions for (<row_num> - <col_num>)" 

        (although this method is more inefficient than the direct approach)
        """
        # direct way
        return GroupTree(row_num).get_num_k_partitions(col_num)

        # # recursive way
        # tree1 = GroupTree(row_num - 1)
        # tree2 = GroupTree(row_num - col_num)
        # return (tree1.get_num_k_partitions(col_num - 1) + 
        #         tree2.get_num_k_partitions(col_num))

class PartitionTree:
    """
    Prereq: num >= 1
    """
    def __init__(self, partition: List[int], group: int, height=0) -> None:
        self.partition = partition
        self.group = group
        self.height = height
        self.children = self.create_children()

    def create_children(self) -> List["GroupTree"]:
        """
        Return the unique numbers in <self.partition> (excluding 1)
        as a list of GroupTrees
        """
        groups = []
        group_nums = []
        for num in self.partition: 
            if num > 1 and num not in group_nums: 
                groups.append(GroupTree(num, self.height + 1))
                group_nums.append(num)
        return groups

    def __str__(self) -> str:
        """
        Note: The number of partitions printed does not include the element itself
        nor is the element itself printed as a partition
        """
        string = "\t" * self.height + f"{self.group}: {self.partition}\n"
        for group in self.children:
            string += f"{str(group)}"
        
        return string

    def get_group_amt(self) -> int:
        """
        Returns the number of unique numbers in the partition
        (excluding 1)
        """
        return len(self.children)

if __name__ == "__main__":
    """
    Note: Printing a GroupTree beyond 8 may not show the entirety of its string output,
    due to its information taking up much of the terminal window
    """
    test_tree = GroupTree(13)
    # print(GroupTree(7))
    print(test_tree.partition_triangle())
    # print(test_tree.get_triangle_row(13))
    # print(test_tree.get_triangle_col(1))
    print(test_tree.get_triangle_entry(4, 12))
    # for i in range(1, 14): print(f"Row {i}: {test_tree.triangle_row_sum(i)}")
    for i in range(1, 14): print(f"Col {i}: {GroupTree(13).triangle_col_sum(i)}")

