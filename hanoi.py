
import math

from copy import deepcopy
from typing import Optional, Tuple

class HanoiTower:
    """
    Represents the Hanoi Tower puzzle with configurable pegs, disks, and state.

    Attributes:
        pegs (int): Number of pegs in the puzzle.
        disks (int): Number of disks in the puzzle.
        state (Optional[list[list[int]]]): Current state of the puzzle.
        parent (Optional[HanoiTower]): Parent state in the search tree.
        last_action (Optional[Tuple[int, int]]): Last move performed.
    """

    def __init__(
        self,
        pegs: int = 3,
        disks: int = 5,
        state: Optional[list[list[int]]] = None,
        parent: Optional["HanoiTower"] = None,
        last_action: Optional[Tuple[int, int]] = None,
    ) -> None:
        """
        Initialize the Hanoi Tower puzzle.

        Args:
            pegs: Number of pegs (default: 3).
            disks: Number of disks (default: 5).
            state: Initial state of the puzzle (default: None).
            parent: Parent state in the search tree (default: None).
            last_action: Last move performed (default: None).

        Raises:
            ValueError: If initialization parameters are invalid.
        """
        self.pegs = pegs  # Uses the setter for validation
        self.disks = disks  # Uses the setter for validation
        self.state = state  # Uses the setter for validation
        self.parent = parent  # Uses the setter for validation
        self.last_action = last_action  # Uses the setter for validation
 
    def __str__(self) -> str:
        """
        Returns a string representation of the Hanoi Tower.

        The representation displays the current state of the pegs and disks in a
        vertical format, with disks represented by their sizes and pegs represented
        by vertical bars (`|`).

        Example:
            For a Hanoi Tower with 3 disks and 3 pegs:
            1     |     |
            2     |     |
            3     |     |

        Returns:
            str: A multi-line string representing the current state of the Hanoi Tower.
        """
        height = self.disks
        disk_width = math.floor(math.log10(self.disks)) + 2 if self.disks > 0 else 1
        rows = []

        for row in range(height - 1, -1, -1):
            row_elements = []
            for peg in range(self.pegs):
                if len(self.state[peg]) > row:
                    # Display the disk size
                    row_elements.append(f"{self.state[peg][row]:{disk_width}}")
                else:
                    # Display the peg (empty space)
                    row_elements.append(" " * (disk_width - 1) + "|")
            rows.append("".join(row_elements))

        return "\n".join(rows)

    def __repr__(self) -> str:
        """
        Returns an unambiguous string representation of the Hanoi Tower.

        This representation is intended for debugging and logging purposes. It provides
        a detailed view of the internal state of the Hanoi Tower.

        Returns:
            str: A string representation of the Hanoi Tower's state.
        """
        return f"HanoiTower(pegs={self.pegs}, disks={self.disks}, state={self.state})"

    def __eq__(self, other: Any) -> bool:
        """
        Compares two HanoiTower instances for equality.

        Two HanoiTower instances are considered equal if their states (i.e., the
        arrangement of disks on pegs) are identical.

        Args:
            other (Any): The object to compare with.

        Returns:
            bool: True if the states are equal, False otherwise.
        """
        if not isinstance(other, HanoiTower):
            return False
        # Compare lengths first for early exit
        if self.pegs != other.pegs or self.disks != other.disks or len(self.state) != len(other.state):
            return False
        # Compare each peg
        for peg1, peg2 in zip(self.state, other.state):
            if peg1 != peg2:
                return False
        return True

    @property
    def pegs(self) -> int:
        """Get the number of pegs."""
        return self._pegs

    @pegs.setter
    def pegs(self, value: int) -> None:
        """Set the number of pegs with validations."""
        if not isinstance(value, int):
            raise ValueError("pegs must be an integer")
        if value < 3:
            raise ValueError("pegs must be an integer greater than or equal to 3")
        self._pegs = value

    @property
    def disks(self) -> int:
        """Get the number of disks."""
        return self._disks

    @disks.setter
    def disks(self, value: int) -> None:
        """Set the number of disks with validation."""
        if not isinstance(value, int):
            raise ValueError("disks must be an integer")
        if value < 1:
            raise ValueError("disks must be an integer greater than or equal to 1")
        self._disks = value

    @property
    def state(self) -> Optional[list[list[int]]]:   
        """Get the current state of the puzzle."""
        return self._state

    @state.setter
    def state(self, value: Optional[list[list[int]]]) -> None:
        """Set the state with validation."""
        if value is not None:
            if not isinstance(value, list):
                raise ValueError("state must be a list of lists")
            if not all(isinstance(peg, list) for peg in value):
                raise ValueError("state must be a list of lists")
            if any(not all(isinstance(disk, int) for disk in peg) for peg in value):
                raise ValueError("state must be a list of lists of integers")
            self._state = value
        else:
            self._state = [[i for i in range(self.disks, 0, -1)]] + [[] for _ in range(self.pegs - 1)]

    @property
    def parent(self) -> Optional["HanoiTower"]:
        """Get the parent state."""
        return self._parent

    @parent.setter
    def parent(self, value: Optional["HanoiTower"]) -> None:
        """Set the parent state with validation."""
        if value is not None:
            if not isinstance(value, HanoiTower):
                raise ValueError("parent must be a HanoiTower instance")
        self._parent = value

    @property
    def last_action(self) -> Optional[Tuple[int, int]]:
        """Get the last action performed."""
        return self._last_action

    @last_action.setter
    def last_action(self, value: Optional[Tuple[int, int]]) -> None:
        """Set the last action with validation."""
        if value is not None:
            if not isinstance(value, tuple):
                raise ValueError("last_action must be a tuple")
            if len(value) != 2:
                raise ValueError("last_action must contain two elements")
            if not all(isinstance(x, int) for x in value):
                raise ValueError("last_action must contain integers")
        self._last_action = value
        
    def move_disk(self, from_peg: int, to_peg: int) -> "HanoiTower":
        """
        Move a disk from one peg to another.

        Args:
            from_peg: Index of the source peg (0-based).
            to_peg: Index of the destination peg (0-based).

        Returns:
            HanoiTower: A new HanoiTower instance representing the updated state.
        """
        if not self._is_valid_peg(from_peg) or not self._is_valid_peg(to_peg):
            raise ValueError("Invalid peg index")

        if not self._is_valid_move(from_peg, to_peg):
            raise ValueError("Invalid move")

        new_state = deepcopy(self.state)
        new_state[to_peg].append(new_state[from_peg].pop())

        return HanoiTower(pegs=self.pegs, disks=self.disks, state=new_state, parent=self, last_action=(from_peg, to_peg))
    
    def get_possible_moves(self) -> List[Tuple[int, int]]:
        """
        Get all possible disk movements from the current state.

        Returns:
            List[Tuple[int, int]]: A list of valid disk movements.
        """
        moves = []
        for from_peg in range(self.pegs):
            for to_peg in range(self.pegs):
                if self._is_valid_move(from_peg, to_peg):
                    moves.append((from_peg, to_peg))
        return moves
    
    def is_goal_state(self) -> bool:
        """
        Check if the current state is a goal state.

        Returns:
            bool: True if the goal state is reached, False otherwise.
        """
        return len(self.state[-1]) == self.disks
    
    def _is_valid_peg(self, peg_index: int) -> bool:
        """Check if a peg index is valid."""
        return 0 <= peg_index < self.pegs
    
    def _is_valid_move(self, from_peg: int, to_peg: int) -> bool:
        """Check if a move is valid."""
        if from_peg == to_peg:
            return False
        if not self.state[from_peg]:
            return False
        if not self.state[to_peg]:
            return True
        return self.state[from_peg][-1] < self.state[to_peg][-1]
    
    
