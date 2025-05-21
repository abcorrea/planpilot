(define
	(problem beluga-problem_15_s57_j11_r2_oc86_f3)
	(:domain beluga)
  (:objects
		; Numbers: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 24, 25, 28, 32}
		n00 - num
		n01 - num
		n02 - num
		n03 - num
		n04 - num
		n05 - num
		n06 - num
		n07 - num
		n08 - num
		n09 - num
		n10 - num
		n11 - num
		n12 - num
		n13 - num
		n14 - num
		n15 - num
		n16 - num
		n17 - num
		n18 - num
		n19 - num
		n20 - num
		n23 - num
		n24 - num
		n25 - num
		n28 - num
		n32 - num
		; trailers:
		beluga_trailer_1 - trailer
		beluga_trailer_2 - trailer
		factory_trailer_1 - trailer
		factory_trailer_2 - trailer
		; Racks:
		rack00 - rack
		rack01 - rack
		; Jigs:
		jig0001 - jig
		jig0002 - jig
		jig0003 - jig
		jig0004 - jig
		jig0005 - jig
		jig0006 - jig
		jig0007 - jig
		jig0008 - jig
		jig0009 - jig
		jig0010 - jig
		jig0011 - jig
		typeE - type
		typeD - type
		typeC - type
		typeB - type
		typeA - type
		; hangars:
		hangar1 - hangar
		hangar2 - hangar
		hangar3 - hangar
		; Beluga flights:
		beluga1 - beluga
		beluga2 - beluga
		beluga3 - beluga
		; Slots for outgoing flights:
		slot0 - slot
		slot1 - slot
		slot2 - slot
		slot3 - slot
		slot4 - slot
		slot5 - slot
		; Production lines:
		pl0 - production-line
		pl1 - production-line
	)
  (:init
		; Number encoding
		; Sizes fitting rack: rack00
		(fit  n00  n04  n04 rack00)
		(fit  n01  n04  n05 rack00)
		(fit  n02  n04  n06 rack00)
		(fit  n03  n04  n07 rack00)
		(fit  n04  n04  n08 rack00)
		(fit  n00  n08  n08 rack00)
		(fit  n05  n04  n09 rack00)
		(fit  n01  n08  n09 rack00)
		(fit  n00  n09  n09 rack00)
		(fit  n06  n04  n10 rack00)
		(fit  n02  n08  n10 rack00)
		(fit  n01  n09  n10 rack00)
		(fit  n07  n04  n11 rack00)
		(fit  n03  n08  n11 rack00)
		(fit  n02  n09  n11 rack00)
		(fit  n00  n11  n11 rack00)
		(fit  n08  n04  n12 rack00)
		(fit  n04  n08  n12 rack00)
		(fit  n03  n09  n12 rack00)
		(fit  n01  n11  n12 rack00)
		(fit  n09  n04  n13 rack00)
		(fit  n05  n08  n13 rack00)
		(fit  n04  n09  n13 rack00)
		(fit  n02  n11  n13 rack00)
		(fit  n11  n04  n15 rack00)
		(fit  n07  n08  n15 rack00)
		(fit  n06  n09  n15 rack00)
		(fit  n04  n11  n15 rack00)
		(fit  n12  n04  n16 rack00)
		(fit  n08  n08  n16 rack00)
		(fit  n07  n09  n16 rack00)
		(fit  n05  n11  n16 rack00)
		(fit  n13  n04  n17 rack00)
		(fit  n09  n08  n17 rack00)
		(fit  n08  n09  n17 rack00)
		(fit  n06  n11  n17 rack00)
		(fit  n15  n04  n19 rack00)
		(fit  n11  n08  n19 rack00)
		(fit  n10  n09  n19 rack00)
		(fit  n08  n11  n19 rack00)
		(fit  n01  n18  n19 rack00)
		(fit  n16  n04  n20 rack00)
		(fit  n12  n08  n20 rack00)
		(fit  n11  n09  n20 rack00)
		(fit  n09  n11  n20 rack00)
		(fit  n02  n18  n20 rack00)
		(fit  n20  n04  n24 rack00)
		(fit  n16  n08  n24 rack00)
		(fit  n15  n09  n24 rack00)
		(fit  n13  n11  n24 rack00)
		(fit  n06  n18  n24 rack00)
		(fit  n24  n04  n28 rack00)
		(fit  n20  n08  n28 rack00)
		(fit  n19  n09  n28 rack00)
		(fit  n17  n11  n28 rack00)
		(fit  n10  n18  n28 rack00)
		(fit  n03  n25  n28 rack00)
		; Sizes fitting rack: rack01
		(fit  n00  n04  n04 rack01)
		(fit  n01  n04  n05 rack01)
		(fit  n02  n04  n06 rack01)
		(fit  n03  n04  n07 rack01)
		(fit  n04  n04  n08 rack01)
		(fit  n00  n08  n08 rack01)
		(fit  n06  n04  n10 rack01)
		(fit  n02  n08  n10 rack01)
		(fit  n01  n09  n10 rack01)
		(fit  n07  n04  n11 rack01)
		(fit  n03  n08  n11 rack01)
		(fit  n02  n09  n11 rack01)
		(fit  n00  n11  n11 rack01)
		(fit  n08  n04  n12 rack01)
		(fit  n04  n08  n12 rack01)
		(fit  n03  n09  n12 rack01)
		(fit  n01  n11  n12 rack01)
		(fit  n10  n04  n14 rack01)
		(fit  n06  n08  n14 rack01)
		(fit  n05  n09  n14 rack01)
		(fit  n03  n11  n14 rack01)
		(fit  n11  n04  n15 rack01)
		(fit  n07  n08  n15 rack01)
		(fit  n06  n09  n15 rack01)
		(fit  n04  n11  n15 rack01)
		(fit  n15  n04  n19 rack01)
		(fit  n11  n08  n19 rack01)
		(fit  n10  n09  n19 rack01)
		(fit  n08  n11  n19 rack01)
		(fit  n01  n18  n19 rack01)
		(fit  n19  n04  n23 rack01)
		(fit  n15  n08  n23 rack01)
		(fit  n14  n09  n23 rack01)
		(fit  n12  n11  n23 rack01)
		(fit  n05  n18  n23 rack01)
		; trailers (Beluga side):
		(empty beluga_trailer_1)
		(at-side beluga_trailer_1 bside)
		(empty beluga_trailer_2)
		(at-side beluga_trailer_2 bside)
		; trailers (Factory side):
		(empty factory_trailer_1)
		(at-side factory_trailer_1 fside)
		(empty factory_trailer_2)
		(at-side factory_trailer_2 fside)
		; Racks 2
		; Rack:rack00
		(at-side rack00 bside)
		(at-side rack00 fside)
		(free-space rack00 n04)
		(in jig0006 rack00)
		(clear jig0006 bside)
		(next-to jig0006 jig0003 bside)
		(next-to jig0003 jig0006 fside)
		(in jig0003 rack00)
		(next-to jig0003 jig0002 bside)
		(next-to jig0002 jig0003 fside)
		(in jig0002 rack00)
		(next-to jig0002 jig0007 bside)
		(next-to jig0007 jig0002 fside)
		(in jig0007 rack00)
		(next-to jig0007 jig0010 bside)
		(next-to jig0010 jig0007 fside)
		(in jig0010 rack00)
		(clear jig0010 fside)
		; Rack:rack01
		(at-side rack01 bside)
		(at-side rack01 fside)
		(free-space rack01 n03)
		(in jig0008 rack01)
		(clear jig0008 bside)
		(next-to jig0008 jig0001 bside)
		(next-to jig0001 jig0008 fside)
		(in jig0001 rack01)
		(next-to jig0001 jig0004 bside)
		(next-to jig0004 jig0001 fside)
		(in jig0004 rack01)
		(next-to jig0004 jig0005 bside)
		(next-to jig0005 jig0004 fside)
		(in jig0005 rack01)
		(next-to jig0005 jig0009 bside)
		(next-to jig0009 jig0005 fside)
		(in jig0009 rack01)
		(clear jig0009 fside)
		; Jigs (size):
		(is_type jig0001 typeA)
		(size jig0001 n04)
		(empty-size jig0001 n04)
		(empty jig0001)
		(is_type jig0002 typeA)
		(size jig0002 n04)
		(empty-size jig0002 n04)
		(empty jig0002)
		(is_type jig0003 typeA)
		(size jig0003 n04)
		(empty-size jig0003 n04)
		(empty jig0003)
		(is_type jig0004 typeA)
		(size jig0004 n04)
		(empty-size jig0004 n04)
		(is_type jig0005 typeA)
		(size jig0005 n04)
		(empty-size jig0005 n04)
		(is_type jig0006 typeB)
		(size jig0006 n08)
		(empty-size jig0006 n08)
		(empty jig0006)
		(is_type jig0007 typeA)
		(size jig0007 n04)
		(empty-size jig0007 n04)
		(is_type jig0008 typeA)
		(size jig0008 n04)
		(empty-size jig0008 n04)
		(empty jig0008)
		(is_type jig0009 typeA)
		(size jig0009 n04)
		(empty-size jig0009 n04)
		(is_type jig0010 typeA)
		(size jig0010 n04)
		(empty-size jig0010 n04)
		(is_type jig0011 typeA)
		(size jig0011 n04)
		(empty-size jig0011 n04)
		; hangars:
		(empty hangar1)
		(empty hangar2)
		(empty hangar3)
		; Flight schedule initial phase:
		(processed-flight beluga1)
		; Flight order:
		(next-flight-to-process beluga1 beluga2)
		(next-flight-to-process beluga2 beluga3)
		; Number of flights: 3
		; Incoming jigs unload order:
		; Finished Flights
		; No already completely finished Flights
		; Current Flight: beluga1
		; 0: jig0011
		(to_unload jig0011 beluga1)
		(in jig0011 beluga1)
		(next_unload jig0011 dummy-jig)
		; To Process Flights
		; Flight: beluga2
		; No jigs
		(to_unload dummy-jig beluga2)
		; Flight: beluga3
		; No jigs
		(to_unload dummy-jig beluga3)
		; Outgoing jigs load order:
		; Finished Flights
		; No already completely finished Flights
		; Current Flight: beluga1
		; (0: typeA) (1: typeA) (2: typeA) (3: typeA)
		(to_load typeA slot0 beluga1)
		(next_load typeA slot0 slot1 beluga1)
		(next_load typeA slot1 slot2 beluga1)
		(next_load typeA slot2 slot3 beluga1)
		(next_load dummy-type slot3 dummy-slot beluga1)
		; To Process Flights
		; 0: typeB
		(to_load typeB slot0 beluga2)
		(next_load dummy-type slot0 dummy-slot beluga2)
		; 0: typeA 1: typeA 2: typeA 3: typeA 4: typeA 5: typeA
		(to_load typeA slot0 beluga3)
		(next_load typeA slot0 slot1 beluga3)
		(next_load typeA slot1 slot2 beluga3)
		(next_load typeA slot2 slot3 beluga3)
		(next_load typeA slot3 slot4 beluga3)
		(next_load typeA slot4 slot5 beluga3)
		(next_load dummy-type slot5 dummy-slot beluga3)
		; Production schedule:
		; Production line: pl0
		; 0: jig0004 1: jig0007 2: jig0010
		(to_deliver jig0004 pl0)
		(next_deliver jig0004 jig0007)
		(next_deliver jig0007 jig0010)
		(next_deliver jig0010 dummy-jig)
		; Production line: pl1
		; 0: jig0005 1: jig0009 2: jig0011
		(to_deliver jig0005 pl1)
		(next_deliver jig0005 jig0009)
		(next_deliver jig0009 jig0011)
		(next_deliver jig0011 dummy-jig)
		; Action cost:
		(= (total-cost ) 0)
	)
  (:goal (and
		; All jigs empty (order defined by production schedule)
		(empty jig0004)
		(empty jig0007)
		(empty jig0010)
		(empty jig0005)
		(empty jig0009)
		(empty jig0011)
		; all Belugas fully unloaded:
		(to_unload dummy-jig beluga1)
		(to_unload dummy-jig beluga2)
		(to_unload dummy-jig beluga3)
		; all Belugas fully loaded:
		(to_load dummy-type dummy-slot beluga1)
		(to_load dummy-type dummy-slot beluga2)
		(to_load dummy-type dummy-slot beluga3)
	))
  (:metric minimize (total-cost))
)