#!/usr/bin/env python3

class Cave(object):
    """ An object that represents a cave (node) in a series of connected caves
        (graph).

        Input:  name of the cave <str>
    """
    def __init__(self, name):
        # The name of the cave
        self.__name = name

        # A list of all the connecting cave objects
        self.__connecting_caves = []

    def __eq__(self, other):
        """ Equal comparison override.

            Input:  other cave <Cave>

            Output: is equal <bool>
        """
        return other.getName() == self.getName()

    def __ge__(self, other):
        """ Greater than or equal comparison override.

            Input:  other cave <Cave>

            Output: is greater than or equal <bool>
        """
        return other.getName() <= self.getName()

    def __gt__(self, other):
        """ Greater than comparison override.

            Input:  other cave <Cave>

            Output: is greater than <bool>
        """
        return other.getName() < self.getName()

    def __le__(self, other):
        """ Less than or equal comparison override.

            Input:  other cave <Cave>

            Output: is less than or equal <bool>
        """
        return other.getName() >= self.getName()

    def __lt__(self, other):
        """ Less than comparison override.

            Input:  other cave <Cave>

            Output: is less than <bool>
        """
        return other.getName() > self.getName()

    def addConnectingCave(self, cave):
        """ Add a cave that connects to this cave.

            Input:  cave <Cave>

            Output: None
        """
        # Check if the given cave is already connected to this cave
        if cave not in self.__connecting_caves:
            self.__connecting_caves.append(cave)
        else:
            print("Cave connection already exists {} --> {}".format(self.getName(), cave.getName()))

    def getConnectingCaves(self):
        """ Return the caves that connect to this cave.

            Input:  None

            Output: connecting caves [cave <Cave>]
        """
        return self.__connecting_caves

    def getName(self):
        """ Return the name of this cave.

            Input:  None

            Output: cave name <str>
        """
        return self.__name

    def isBigCave(self):
        """ Return if this is a big cave or not.

            Input:  None

            Output: is a big cave <bool>
        """
        return not self.isLittleCave()

    def isLittleCave(self):
        """ Return if this is a little cave or not.

            Input:  None

            Output: is a little cave <bool>
        """
        return self.__name == self.__name.lower()
