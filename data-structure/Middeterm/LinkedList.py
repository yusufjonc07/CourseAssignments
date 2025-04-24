class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insertAtEnd(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def deleteAtPosition(self, pos):
        if pos < 1 or not self.head:
            return
        if pos == 1:
            self.head = self.head.next
            return
        temp = self.head
        for just in range(pos - 2):
            if not temp.next:
                return
            temp = temp.next
        if temp.next:
            temp.next = temp.next.next

    def display(self):
        temp = self.head
        while temp:
            print(temp.data, end=" -> ")
            temp = temp.next
        print("None")


# Example
ll = LinkedList()
ll.insertAtEnd(1)
ll.insertAtEnd(2)
ll.insertAtEnd(3)
ll.display()        # 1 -> 2 -> 3 -> None

ll.deleteAtPosition(2)
ll.display()        # 1 -> 3 -> None
