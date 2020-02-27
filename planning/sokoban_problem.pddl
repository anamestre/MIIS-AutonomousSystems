(define (problem boxes)
	(:domain sokoban)
	(:objects pos1 pos2 pos3 pos4 pos5 pos6 pos7 pos8 pos9 pos10 pos11 pos12 pos13 pos14 pos15 - position)
	(:init  
		(haswall pos1)
		(haswall pos2)
		(haswall pos3)
		(haswall pos4)
		(haswall pos5)
		
		(haswall pos6)
		(at agent pos7)
		(hasbox pos8)
		(haswall pos10)
		
		(haswall pos11)
		(haswall pos12)
		(haswall pos13)
		(haswall pos14)
		(haswall pos15)
		
		(= (num_teleports) 0))
		
	(:goal (and(hasbox pos9)))
)