Check which symbols match the pattern the model was trained on
-----------------------------------------------------------------

http://localhost:8002/pattern/DEZ:DE



{"symbol":"DEZ:DE","pattern_detected":true}



{"symbol":"VIB3:DE","pattern_detected":false}


the python scripts allow for batch checking of all the companies, the results are stored in symbolpatterns or symbolpatterns2
the difference between these tables is the datatype (jsonb or normal)
