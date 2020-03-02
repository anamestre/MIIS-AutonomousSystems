(define (domain sokoban)
	(:requirements :adl :typing)
	(:types position)
	(:constants agent)
	(:predicates 
			(at ?elem ?pos)							;; Agent is at position pos
			(hasbox ?pos - position)				;; Position pos has a box
			(next ?pos1 ?pos2 - position)			;; Pos1 is next to pos2
			(double_next ?pos1 ?pos2 - position)	;; Pos1 is next to pos2 and pos3 is next to pos2 all in line
			(haswall ?pos - position)				;; Position pos has a wall
			(first_teleport)
			(second_teleport))
	;;(:functions 
	;;		(num_teleports))						;; Global function to know how many teleports have been done
	
	(:action goto									;; Move agent from position "from" to "to"
		:parameters (?from ?to - position)
		:precondition (and (at agent ?from) (not (hasbox ?to)) (or(next ?from ?to) (next ?to ?from))(not (haswall ?to)))
		:effect (and (at agent ?to) (not (at agent ?from))))
	
	(:action pushbox								;; Push box from position "bos_pos" to "to".
		:parameters (?from ?box_pos ?to - position)
		:precondition (and (at agent ?from) (hasbox ?box_pos) (not (hasbox ?to)) 
					  (or
						(and(next ?from ?box_pos) (next ?box_pos ?to) (double_next ?from ?to))
						(and(next ?to ?box_pos ) (next ?box_pos ?from) (double_next ?to ?from))
					  )
					  (not (haswall ?to)))
		:effect (and (not (hasbox ?box_pos)) (hasbox ?to) (not (at agent ?from)) (at agent ?box_pos)))
	
	;;(:action teleport								;; Move agent in a teleporting way from "from" to "to".
	;;	:parameters (?from ?to - position)
	;;	:precondition (and (at agent ?from) (not (hasbox ?to)) (not (haswall ?to)) (< (num_teleports) 2))
	;;	:effect (and (increase (num_teleports) 1) (not (at agent ?from)) (at agent ?to)))
	
	(:action teleport
		:parameters (?from ?to - position)
		:precondition (and (at agent ?from) (not (hasbox ?to)) (not (haswall ?to)) (not (first_teleport)) (not (second_teleport)))
		:effect (and (first_teleport) (not (at agent ?from)) (at agent ?to)))
	
	(:action teleport
		:parameters (?from ?to - position)
		:precondition (and (at agent ?from) (not (hasbox ?to)) (not (haswall ?to)) (first_teleport) (not (second_teleport)))
		:effect (and (second_teleport) (not (at agent ?from)) (at agent ?to)))
)