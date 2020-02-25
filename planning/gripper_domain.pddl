(define (domain gripper)
(:requirements :typing)
(:types room ball gripper)
(:constants left right - gripper)
(:predicates (at-robot ?r - room)(at ?b - ball ?r - room)(free ?g - gripper)
(carry ?o - ball ?g - gripper))
(:action move
:parameters (?from ?to - room)
:precondition (at-robot ?from)
:effect (and (at-robot ?to) (not (at-robot ?from))))
(:action pick
:parameters (?obj - ball ?room - room ?gripper - gripper)
:precondition (and (at ?obj ?room) (at-robot ?room) (free ?gripper))
:effect (and (carry ?obj ?gripper) (not (at ?obj ?room)) (not (free ?gripper))))
(:action drop
:parameters (?obj - ball ?room - room ?gripper - gripper)
:precondition (and (carry ?obj ?gripper) (at-robot ?room))
:effect (and (at ?obj ?room) (free ?gripper) (not (carry ?obj ?gripper)))))