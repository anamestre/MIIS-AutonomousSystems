(define (domain sokoban)
	(:requirements :adl :typing)
	(:types position)
	(:constants agent)
	(:predicates (at ?elem ?pos)
				 (hasbox ?pos - position)
				 (next ?pos1 ?pos2 - position)
				 (double_next ?pos1 ?pos2 - position)
				 (haswall ?pos - position))
	(:functions (num_teleports))
	(:action goto
		:parameters (?from ?to - position)
		:precondition (and (at agent ?from) (not (hasbox ?to)) (next ?from ?to) (not (haswall ?to)))
		:effect (and (at agent ?to) (not (at agent ?from))))
	
	(:action pushbox
		:parameters (?from ?box_pos ?to - position)
		:precondition (and (at agent ?from) (hasbox ?box_pos) (not (hasbox ?to)) 
					  (next ?from ?box_pos) (next ?box_pos ?to) (double_next ?from ?to)
					  (not (haswall ?to)))
		:effect (and (not (hasbox ?box_pos)) (hasbox ?to) (not (at agent ?from)) (at agent ?box_pos)))
	
	(:action teleport
		:parameters (?from ?to - position)
		:precondition (and (at agent ?from) (not (hasbox ?to)) (not (haswall ?to)) (< (num_teleports) 2))
		:effect (and (increase (num_teleports) 1) (not (at agent ?from)) (at agent ?to)))
)