HAI
	WAZZUP
		I HAS A choice
		I HAS A input
	BUHBYE

	BTW if w/o MEBBE, 1 only, everything else is invalid
	VISIBLE "1. Compute age"
	VISIBLE "2. Compute tip"
	VISIBLE "3. Compute square area"
	VISIBLE "0. Exit"

	VISIBLE "Choice: "
	GIMMEH choice

	BOTH SAEM choice AN 1
	O RLY?
		YA RLY
			VISIBLE "Enter birth year: "
			GIMMEH input
			VISIBLE DIFF OF 2022 AN input
BTW
	BTW uncomment this portion if you have MEBBE
	BTW else, this portion should be ignored

BTW		MEBBE BOTH SAEM choice AN 2
BTW			VISIBLE "Enter bill cost: "
BTW			GIMMEH input
BTW			VISIBLE "Tip: " PRODUKT OF input AN 0.1
BTW		MEBBE BOTH SAEM choice AN 3
BTW			VISIBLE "Enter width: "
BTW			GIMMEH input
BTW			VISIBLE "Square Area: " PRODUKT OF input AN input
BTW		MEBBE BOTH SAEM choice AN 0
BTW			VISIBLE "Goodbye"
BTW
		NO WAI
			VISIBLE "Invalid Input!"
	OIC

	DIFFRINT BIGGR OF 3 AN choice AN 3
	O RLY?
		YA RLY
			VISIBLE "Invalid input is > 3."
	OIC

KTHXBYE