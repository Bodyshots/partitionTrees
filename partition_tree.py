from sage.all import Partitions
from typing import List

class GroupTree:
    def __init__(self, num: int, height=0):
        self.element = num
        self.height = height
        self.children = self.create_children()

    def create_children(self) -> List["PartitionTree"]:
        return [PartitionTree(partition, self.element, self.height + 1) for partition in Partitions(self.element)[1:]]

    def __str__(self):
        string = "\t" * self.height + f"{self.element} ({len(self.children)} partition(s))\n"
        for partition in self.children:
            string += f"{str(partition)}"

        return string

    def get_partition_num(self): return len(self.children) + 1

    def get_partitions(self): 
        string = f"{self.get_partition_num()} partition(s) for {self.element}:\n"
        string += f"\t{str([self.element])}\n"
        for partition in self.children:
            string += f"\t{str(partition.partition)}\n"
        return string

    def get_num_k_partitions(self, k: int):
        count = 0
        if k == 1: count = 1
        else:
            for partition in self.children: 
                if len(partition.partition) == k: count += 1

        print(f"{self.element}: Number of {k}-length partitions: {count}")
        return count

class PartitionTree:
    """
    Prereq: num >= 1
    """
    def __init__(self, partition: List[int], group: int, height=0):
        self.partition = partition
        self.group = group
        self.height = height
        self.children = self.create_children()

    def create_children(self):
        groups = []
        group_nums = []
        for num in self.partition: 
            if num > 1 and num not in group_nums: 
                groups.append(GroupTree(num, self.height + 1))
                group_nums.append(num)
        return groups

    def __str__(self):
        string = "\t" * self.height + f"{self.group}: {self.partition}\n"
        for group in self.children:
            string += f"{str(group)}"
        
        return string

    def get_group_amt(self): return len(self.children)

if __name__ == "__main__":
    """
    Note: Printing a GroupTree beyond 8 may not show the entirety of its string output,
    due to its information taking up much of the terminal window
    """
    for j in range(1, 7):
        for i in range(1, 13):
            test = GroupTree(i)
            test.get_num_k_partitions(j)
        print("\n")
