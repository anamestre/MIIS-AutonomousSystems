(define (problem monkey2)
	(:domain monkey)
	(:objects pos1 pos2 pos3 bananas monkey chair)
	(:init  (position pos1)
			(position pos2)
			(position pos3)
			(at monkey pos1)
			(at chair pos2)
			(at bananas pos3))
	(:goal (and(hasbananas))))