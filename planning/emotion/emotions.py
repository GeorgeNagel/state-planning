from emotion.mood import Mood


class Emotion(object):
    def __init__(self, amount):
        """amount - how acute is the emotional reaction."""
        if amount < 0 or amount > 1:
            raise ValueError()
        self.amount = amount

    def __str__(self):
        return "%s (%s)" % (self.__class__.__name__, self.amount)

    def __repr__(self):
        return self.__str__()

    def _to_pad(self):
        raise NotImplementedError

    def to_mood(self):
        """
        Convert the emotion to PAD space
        http://infoscience.epfl.ch/record/199429/files/510.pdf
        pg. 25
        """
        p, a, d = self._to_pad()
        mood = Mood(p*self.amount, a*self.amount, d*self.amount)
        return mood


class Joy(Emotion):
    """Because something good happened."""
    def _to_pad(self):
        return (.4, .2, .1)


class Hope(Emotion):
    """About the possibility of something good happening."""
    def _to_pad(self):
        return (.2, .2, -.1)


class Relief(Emotion):
    """Because a feared bad thing didn't happen."""
    def _to_pad(self):
        return (.2, -.3, .4)


class Pride(Emotion):
    """About a self-initiated praiseworthy act."""
    def _to_pad(self):
        return (.4, .3, .3)


class Gratitude(Emotion):
    """About an other-initiated praiseworthy act."""
    def _to_pad(self):
        return (.4, .2, -.3)


class Love(Emotion):
    """Because a person finds someone or something appealing."""
    def _to_pad(self):
        return (.3, .1, .2)


class HappyFor(Emotion):
    """Because something good happened to a liked person."""
    def _to_pad(self):
        return (.4, .2, .2)


class Gloating(Emotion):
    """Because something bad happened to a person who isn't liked."""
    def _to_pad(self):
        return (.3, -.3, -.1)


class Distress(Emotion):
    """Because something bad happened."""
    def _to_pad(self):
        return (-.4, -.2, -.5)


class Fear(Emotion):
    """About the possibility of something bad happening."""
    def _to_pad(self):
        return (-.64, .6, -.43)


class Disappointment(Emotion):
    """Because a hoped-for good thing didn't happen."""
    def _to_pad(self):
        return (-.3, .1, -.4)


class Remorse(Emotion):
    """About a self-initiated blameworthy act."""
    def _to_pad(self):
        return (-.3, .1, -.6)


class Anger(Emotion):
    """About an other-initiated blameworthy act."""

    def _to_pad(self):
        return (-.51, .59, .25)


class Hate(Emotion):
    """Because a person finds someone or something unappealing."""
    def _to_pad(self):
        return (-.6, .6, .3)


class SorryFor(Emotion):
    """Because something bad happened to a liked person."""
    def _to_pad(self):
        return (-.4, -.2, -.5)


class Resentment(Emotion):
    """Because something good happened to a person not liked."""
    def _to_pad(self):
        return (-.2, -.3, -.2)
