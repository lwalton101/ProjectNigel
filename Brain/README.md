## Threads

Voice input thread
Intent Detection thread
Intent execution thread
Camera thread(bit far ahead)

When voice input:
  stop the intent detection and execution and start the detection again

## Is any other language viable?
python is quite slow and I do not enjoy using it.
we can train the ai in python, but run in other langauges. we need to do this to use the Bert Models

python - good library support, slow slow slow, we have very limited hardware

js - not better than python for a task like this
c# - possible, TensorFlowSharp and TensorFlow.NET exist, i like it's package manager
java - no
c++ - i dislike this but it is fast and there is some kind of official tensorflow support maybe??, but vad will be difficult
