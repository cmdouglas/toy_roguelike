class Stackable:
    stack_size = 1
    max_stack_size = None

    def merge_with_stack(self, other):
        assert type(other) == type(self)

        if (self.max_stack_size is not None and
           self.stack_size + other.stack_size > self.max_stack_size):
            raise StackTooLargeException()

        self.stack_size += other.stack_size

    def split_stack(self, new_size):
        assert new_size <= self.stack_size

        new_stack = type(self)()
        new_stack.stack_size = new_size
        self.stack_size -= new_size

        return new_stack, self

    def pop_from_stack(self, count=1):
        return self.split_stack(count)[0]

    def is_empty(self):
        return self.stack_size <= 0


class StackTooLargeException(Exception):
    pass
