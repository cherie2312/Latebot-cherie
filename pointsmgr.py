class PointsMgr:
	def __init__(self):
		import telepot
		from dbhelper import DBHelper

		global db
		db = DBHelper()

		TOKEN ="517792218:AAE4xZpbaEhSeI8hvOFY9MRtgJc5IbyfW8w"
		global bot
		bot = telepot.Bot(TOKEN)

	def add(self,late_time,owner_id):
		late_int = int(late_time)

		if late_int < 5:
			points_added = 0
			msg_txt = 'Give chance pls'
			
			

		elif 5 <= late_int < 10:
			points_added = late_int
			msg_txt = 'Points added = ' + str(points_added) 
			

		elif 10 <= late_int < 15:
			points_added = round(late_int*1.5,0)
			msg_txt = 'Points added = ' + str(late_int) + '*1.5 = ' + str(points_added) 
			

		elif 15 <= late_int < 20:
			points_added = round(late_int*2,0)
			msg_txt = 'Points added = ' + str(late_int) + '*1.5 = ' + str(points_added) 
			

		elif 20 <= late_int < 25:
			points_added = round(late_int*2.5,0)
			msg_txt = 'Points added = ' + str(late_int) + '*1.5 = ' + str(points_added) 
			

		elif 25 <= late_int < 30:
			points_added = round(late_int*3,0)
			msg_txt = 'Points added = ' + str(late_int) + '*1.5 = ' + str(points_added) 
			

		
		elif  late_int >= 30:
			points_added = round(late_int*4,0)
			msg_txt = 'Points added = ' + str(late_int) + '*1.5 = ' + str(points_added) 
			

		print(points_added)
		db.add_point(points_added,owner_id)
		bot.sendMessage(owner_id, msg_txt)
		#return points_added
		return msg_txt
	
	
	def tally(self,owner_id):
		try:
			tally = "\n".join(db.get_points(owner_id))
					
			bot.sendMessage(owner_id, tally)
			return tally

		except Exception as e:
			print e


	def total(self,owner_id):
		try:
			total = db.get_total(owner_id)[0]
			msg_txt = "total:" + str(total)

			bot.sendMessage(owner_id, msg_txt)
			return total

		except Exception as e:
			print e

	def redeem(self,query_data,from_id):
		redeem_amt = int(query_data)*-10
		
		try: 
			points_avail = db.get_total(from_id)[0]
			

			if redeem_amt*-1 > points_avail:
				pass

			else:
				msg_txt = 'Points redeemed = ' + str(redeem_amt*-1)
				db.add_point(str(redeem_amt),from_id)
				#bot.sendMessage(from_id, msg_txt)

				
				
                

		except Exception as e:
			print e
                