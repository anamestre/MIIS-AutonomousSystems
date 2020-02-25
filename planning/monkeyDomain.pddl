(define (domain monkey)
	(:requirements :adl :typing)
	(:constants monkey bananas chair)
	(:predicates (at ?m ?p)(position ?p) (hasbananas) (onchair))
	
	(:action goto
		:parameters (?from ?to)
		:precondition (and (position ?from) (position ?to) (at monkey ?from))
		:effect (and (at monkey ?to) (not (at monkey ?from))))
	
	(:action pushChair
		:parameters (?from ?to)
		:precondition (and (position ?from) (position ?to) (at chair ?from) (at monkey ?from) (not (onchair)))
		:effect (and (at chair ?to) (at monkey ?to) (not (at monkey ?from)) (not (at chair ?from))))
	
	(:action climb
		:parameters (?pos)
		:precondition (and (position ?pos) (at chair ?pos) (at monkey ?pos))
		:effect (and (onchair)))
	(:action take
		:parameters (?pos)
		:precondition (and (onchair) (at bananas ?pos) (position ?pos) (at chair ?pos) )
		:effect (and (hasbananas)))
)
		