from rxsignal.observable import feedback_subject

def aperiodic_filter(signal, timeconst, delta, init=0):
	state = feedback_subject()
	error = signal - state
	newstate = (state + error * delta / timeconst)
	newstate.subscribe(lambda x: state.on_next(x))
	state.on_next(init)
	return state
