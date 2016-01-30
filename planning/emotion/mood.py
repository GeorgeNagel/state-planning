class Mood(object):
    """
    PAD mid-term mental state.
    p - Pleasure
    a - Arousal
    d - Dominance
    """
    def __init__(self, p, a, d):
        self.p = p
        self.a = a
        self.d = d

    def add_mood(self, other):
        self.p = self.p + other.p
        self.a = self.a + other.a
        self.d = self.d + other.d

    def update_from_emotions(self, emotions):
        for emotion in emotions:
            emotion_mood = emotion.to_mood()
            self.add_mood(emotion_mood)

    def __str__(self):
        return "%s (%s)" % (self.type, self.amount)

    @property
    def amount(self):
        return (self.p**2.0 + self.a**2.0 + self.d**2.0)**0.5

    @property
    def type(self):
        """
        Value to return when cast to a string.

        http://infoscience.epfl.ch/record/199429/files/510.pdf
        pg. 24.
        """
        if self.p >= 0:
            if self.a >= 0:
                if self.d >= 0:
                    return "Exuberant"
                else:
                    return "Dependent"
            else:
                if self.d >= 0:
                    return "Relaxed"
                else:
                    return "Docile"
        else:
            if self.a >= 0:
                if self.d >= 0:
                    return "Hostile"
                else:
                    return "Anxious"
            else:
                if self.d >= 0:
                    return "Disdainful"
                else:
                    return "Bored"
