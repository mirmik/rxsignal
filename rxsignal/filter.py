from rxsignal.observable import FeedbackSubject


def aperiodic_filter(signal, timeconst, delta, init=0):
    state = FeedbackSubject(init)
    error = signal - state
    newstate = (state + error * delta / timeconst)
    return state.loop(newstate)


def rxintegral(signal, delta, init=0):
    state = FeedbackSubject(init)
    newstate = (state + signal * delta)
    return state.loop(newstate)
