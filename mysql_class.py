import mysql.connector
import os
import uuid
from datetime import datetime, timedelta


class StartUpDB:
    def __init__(self) -> None:

        self.db = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("MEMBERNAME"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"))

        self.cursor = self.db.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS server (
                            guild_id BIGINT UNIQUE, 
                            admin_role BIGINT, 
                            moderator_role BIGINT, 
                            supporter_role BIGINT, 
                            global_channel BIGINT, 
                            language TINYTEXT,
                            vip TINYTEXT,
                            welcome_message VARCHAR(255),
                            welcome_channel BIGINT
                            )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                            case_id  VARCHAR(20) UNIQUE,
                            guild_id BIGINT, 
                            user_id BIGINT, 
                            case_creator BIGINT, 
                            date TINYTEXT, 
                            reason VARCHAR(255),
                            info VARCHAR(255), 
                            changes LONGTEXT,
                            type TINYTEXT,
                            case_status VARCHAR(255)
                            )''')      

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ticket_system (
                            ticket_message_id BIGINT UNIQUE,
                            type TINYTEXT,
                            guild_id BIGINT,
                            ticket_channel_id BIGINT,
                            ticket_category_id BIGINT,
                            b_one_label TINYTEXT,
                            b_two_label TINYTEXT,
                            b_three_label TINYTEXT,
                            b_one_id BIGINT,
                            b_two_id BIGINT,
                            b_three_id BIGINT
                            )''') 

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                            ticket_id BIGINT UNIQUE,
                            guild_id BIGINT,
                            ticket_creator BIGINT, 
                            created_at TINYTEXT,
                            members VARCHAR(255)
                            )''')  

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS dashboard_sessions (
                            session_id VARCHAR(20) UNIQUE,
                            token TEXT,
                            refresh_token TEXT,
                            token_expires_at TIMESTAMP,
                            user_id TEXT)''')


        self.cursor.execute('''CREATE TABLE IF NOT EXISTS level_system (
                            user_id BIGINT,
                            guild_id BIGINT,
                            level_points BIGINT,
                            level BIGINT,
                            last_msg_xp TIMESTAMP)''')


        self.cursor.execute('''CREATE TABLE IF NOT EXISTS giveaway (
                            giveaway_id INTEGER,
                            time BIGINT,
                            prize TEXT,
                            message BIGINT,
                            channel_id BIGINT,
                            guild_id BIGINT,
                            participants TEXT,
                            winners INTEGER,
                            finished BOOL,
                            requierement VARCHAR(1500))''')         

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS buttons (
                            b_extra_one VARCHAR(50),
                            b_extra_two VARCHAR(50),
                            b_extra_three VARCHAR(50),
                            b_extra_four VARCHAR(250),
                            b_extra_five VARCHAR(50),
                            guild_id BIGINT)''')  
                     
        self.db.commit()




    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################


class BotDB:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("MEMBERNAME"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"))


        self.cursor = self.db.cursor()



    ##################################################################################################################
                                                # Q U E R Y # 
    ##################################################################################################################

    # SERVER TABLE #
    def query_server_table(self, guild_id):
        '''Output Order\n\n
        0 = Guild ID\n
        1 = Admin Role ID\n
        2 = Moderator Role ID\n
        3 = Supporter Role ID\n
        4 = Global Channel ID\n
        5 = Language\n
        6 = VIP'''

        self.cursor.execute('SELECT guild_id, admin_role, moderator_role, supporter_role, global_channel, language, vip from server WHERE guild_id = %s', (guild_id,))
        output = self.cursor.fetchone()
        if output is not None:
            return output
        else:
            output = None

    ##################################################################################################################

    def query_all_global_channels(self):

        self.cursor.execute('SELECT global_channel FROM server')
        output = self.cursor.fetchall()

        if output is not None:
            return output
        else:
            output = None


    ##################################################################################################################

    ##################################################################################################################

    def query_custom_one_slot(self, select_value, table, search_value):

        self.cursor.execute(f'SELECT {select_value} from {table} WHERE guild_id = %s', (search_value,))
        output = self.cursor.fetchone()

        if output is not None:
            return output
        else:
            output = None

    ##################################################################################################################

    def query_all_case_ids(self, member_id, guild_id):
        ''''
        Input -> Member ID | Guild ID\n\n
        Ouput\n
        0 = Case IDs
        '''
        self.cursor.execute('SELECT case_id FROM history WHERE user_id = %s AND guild_id = %s', (member_id, guild_id,))
        output = self.cursor.fetchall()

        if output is not None:
            return output
        else:
            output = None

    ##################################################################################################################

    def query_all_case_ids_with_type(self, member_id, guild_id, c_type):
        ''''
        Input -> Member ID | Guild ID | Type\n\n
        Ouput\n
        0 = Case IDs
        '''
        self.cursor.execute('SELECT case_id FROM history WHERE user_id = %s AND guild_id = %s AND type = %s', (member_id, guild_id, c_type,))
        output = self.cursor.fetchall()

        if output is not None:
            return output
        else:
            output = None

    ##################################################################################################################

    def query_case_reason_and_type(self, case_id, guild_id):
        '''
        Input -> Case ID | Guild ID\n\n
        Output Order\n
        0 = Info\n
        1 = Type'''

        self.cursor.execute('SELECT info, type FROM history WHERE case_id = %s AND guild_id = %s', (case_id, guild_id,))
        output = self.cursor.fetchone()

        if output is not None:
            return output
        else:
            output = None

    ##################################################################################################################

    def query_case_all(self, case_id, guild_id):
        '''
        Input -> Case ID | Guild ID\n
        Output Order\n
        0 = Case Creator\n
        1 = Date\n
        2 = Reason\n
        3 = Info\n
        4 = Changes\n
        5 = Type\n
        6 = Case Status\n
        '''

        self.cursor.execute('SELECT case_creator, date, reason, info, changes, type, case_status FROM history WHERE case_id = %s AND guild_id = %s', (case_id, guild_id,))
        output = self.cursor.fetchone()

        if output is not None:
            return output
        else:
            output = None

            
    ##################################################################################################################

    def query_case_with_user(self, target_id, guild_id, case_id):
        '''
        Input -> Member ID | Guild ID | Case ID\n\n
        Output Order\n
        0 = Case Creator\n
        1 = Date\n
        2 = Reason\n
        3 = Info\n
        4 = Changes\n
        5 = Type\n
        6 = Case Status\n
        '''
        
 
        self.cursor.execute('SELECT case_creator, date, reason, info, changes, type, case_status FROM history WHERE case_id = %s AND guild_id = %s', (case_id, guild_id,))
        output = self.cursor.fetchone()

        if output is not None:
            return output
        else:
            output = None

    ##################################################################################################################

    def query_all_cases_via_case_id_with_offset(self, offset_count, target_id, guild_id):

        self.cursor.execute(f'SELECT case_id, type FROM moderation WHERE user_id = %s AND guild_id = %s LIMIT 25 OFFSET {25 * offset_count}', (target_id, guild_id,))
        output = self.cursor.fetchall()

        if output is not None:
            return output
        else:
            output = None

    ##################################################################################################################

    def query_case_informations(self, target_id, guild_id, case_id):

        self.cursor.execute('''SELECT warned_by, reason, date, last_edit_time, last_edit_by FROM moderation
                             WHERE user_id = %s AND guild_id = %s AND case_id = %s''',
                             (target_id, guild_id, case_id,))
        output = self.cursor.fetchone()

        if output is not None:
            return output
        else:
            output = None

    ##################################################################################################################

    def query_ticket_informations(self, ticket_id):
        
        '''Input Order -> Ticket ID
        Output Order\n
        0 = Ticket Creator ID\n
        1 = Created at\n
        2 = Members'''

        self.cursor.execute('''SELECT ticket_creator, created_at, members FROM tickets
                             WHERE ticket_id = %s''',
                             (ticket_id,))
        output = self.cursor.fetchone()

        if output is not None:
            return output
        else:
            output = None


    ##################################################################################################################

    def query_ticket_system(self, guild_id):

        '''Input -> Guild ID\n\n
        Output Order\n
        0 = Ticket Message ID\n
        1 = Ticket Type\n
        2 = Guild ID\n
        3 = Ticket Channel ID\n
        4 = Ticket Category ID\n
        5 = Button 1 Label\n
        6 = Button 2 Label\n
        7 = Button 3 Label\n
        8 = Button 1 ID\n
        9 = Button 2 ID\n
        10 = Button 3 ID\n'''

        self.cursor.execute('SELECT ticket_message_id, type , guild_id, ticket_channel_id, ticket_category_id, b_one_label, b_two_label, b_three_label, b_one_id, b_two_id, b_three_id FROM ticket_system WHERE guild_id = %s',
                            (guild_id,))
        output = self.cursor.fetchone()
        
        if output is not None:
            return output
        else:
            output = None


    ##################################################################################################################

    def query_tickets_by_user(self, guild_id, user_id):
        '''Input Order -> Guild ID | Ticket Creator ID\n\n
        '''
    
        self.cursor.execute('SELECT ticket_id FROM tickets WHERE guild_id = %s AND ticket_creator = %s', (guild_id, user_id,))
        output = self.cursor.fetchall()

        if output is not None:
            return output
        else:
            output = None

    ##################################################################################################################
                                                # U P D A T E # 
    ##################################################################################################################

    def update_custom_one_slot(self, table, update_parameter, update_value, guild_id):
        
        self.cursor.execute(f'UPDATE {table} SET {update_parameter} = %s WHERE guild_id = %s', (update_value, guild_id))

        self.db.commit()
        return True
    
    ##################################################################################################################

    def update_administrator_role(self, role_id, guild_id):
        self.cursor.execute("UPDATE server SET admin_role = %s WHERE guild_id = %s", (role_id, guild_id,))
        self.db.commit()
        return True

    ##################################################################################################################

    def update_moderator_role(self, role_id, guild_id):
        self.cursor.execute("UPDATE server SET moderator_role = %s WHERE guild_id = %s", (role_id, guild_id,))
        self.db.commit()
        return True
    
    ##################################################################################################################

    def update_supporter_role(self, role_id, guild_id):
        self.cursor.execute("UPDATE server SET supporter_role = %s WHERE guild_id = %s", (role_id, guild_id,))
        self.db.commit()
        return True

    ##################################################################################################################

    def update_language(self, language, guild_id):
        self.cursor.execute("UPDATE server SET language = %s WHERE guild_id = %s", (language, guild_id,))
        self.db.commit()
        return True 
    
    ##################################################################################################################

    def update_global_channel(self, global_channel, guild_id):
        self.cursor.execute("UPDATE server SET global_channel = %s WHERE guild_id = %s", (global_channel, guild_id,))
        self.db.commit()
        return True 
    
    ##################################################################################################################

    def update_case_reason(self, reason, edit_at, edit_by, case_id, guild_id):
        self.cursor.execute('UPDATE moderation SET reason = %s, last_edit_time = %s, last_edit_by = %s WHERE case_id = %s AND guild_id = %s',
                             (reason, edit_at, edit_by, case_id, guild_id,))
        self.db.commit()
        return True 
    
    ##################################################################################################################

    def update_case(self, reason, changes, case_id, guild_id):
        '''
        Input\n
        Update Data -> Reason | Changes\n
        Search Data -> Case ID | Guild ID
        '''
        self.cursor.execute('UPDATE history SET reason = %s, changes = %s WHERE case_id = %s AND guild_id = %s',
                             (reason, changes, case_id, guild_id,))
        self.db.commit()
        return True 

    ##################################################################################################################

    def update_case_status(self, case_status, guild_id, case_id):
        '''
        Input\n
        Update Data -> Case Status\n
        Search Date -> Guild ID | Case ID'''

        self.cursor.execute('UPDATE history SET case_status = %s WHERE guild_id = %s AND case_id = %s',
                            (case_status, guild_id, case_id,))
        
        self.db.commit()
        return True
    
    ##################################################################################################################

    def update_ticket_system_after_create(self, ticket_channel, ticket_category, b_one_id, b_two_id, b_three_id, guild_id):
        '''
        Input\n
        Update Data -> Ticket Channel ID | Ticket Category ID | Button 1 ID | Button 2 ID | Button 3 ID\n
        Search Date -> Guild ID
        '''

        self.cursor.execute('UPDATE ticket_system SET ticket_channel_id = %s, ticket_category_id = %s, b_one_id = %s, b_two_id = %s, b_three_id = %s WHERE guild_id = %s',
                            (ticket_channel, ticket_category, b_one_id, b_two_id, b_three_id, guild_id,))
        self.db.commit()
        return True
    

    ##################################################################################################################
                                                # I N S E R T # 
    ##################################################################################################################
    
    def insert_custom_one_slot(self, table, update_parameter, guild_id, update_value):
        
        self.cursor.execute(f'INSERT INTO {table} (guild_id, {update_parameter}) VALUES (%s, %s)', (guild_id, update_value,))

        self.db.commit()
        return True
    
    ##################################################################################################################

    def insert_administrator_role(self, guild_id, role_id):
        self.cursor.execute('INSERT INTO server (guild_id, admin_role) VALUES (%s, %s)', (guild_id, role_id,))
        self.db.commit()
        return True
    
    ##################################################################################################################

    def insert_moderator_role(self, guild_id, role_id):
        self.cursor.execute('INSERT INTO server (guild_id, moderator_role) VALUES (%s, %s)', (guild_id, role_id,))
        self.db.commit()
        return True
    
    ##################################################################################################################

    def insert_supporter_role(self, guild_id, role_id):
        self.cursor.execute('INSERT INTO server (guild_id, supporter_role) VALUES (%s, %s)', (guild_id, role_id,))
        self.db.commit()
        return True

    ##################################################################################################################

    def insert_language(self, guild_id, language):
        self.cursor.execute('INSERT INTO server (guild_id, language) VALUES (%s, %s)', (guild_id, language,))
        self.db.commit()
        return True

    ##################################################################################################################

    def insert_case(self, guild_id, member_id, moderator_id, current_time, reason, info, random_id, entry_type, case_status):
        '''
        Input Order\n\n
        Guild ID\n
        Member ID\n
        Moderator ID\n
        Date\n
        Reason\n
        Info\n
        Case ID\n
        Type\n
        Case Status\n
        '''
        self.cursor.execute('INSERT INTO history (guild_id, user_id, case_creator, date, reason, info, case_id, type, case_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                            (guild_id, member_id, moderator_id, current_time, reason, info, random_id, entry_type, case_status,))
        self.db.commit()
        return True

    ##################################################################################################################

    def insert_ticket_system(self, ticket_message_id, t_type, guild_id, ticket_channel_id, ticket_category_id, b_one_label, b_two_label, b_three_label, b_one_id, b_two_id, b_three_id):
        '''
        Input Order\n\n
        Ticket Message ID\n
        Ticket Type\ns
        Guild ID ID\n
        Channel ID\n
        Category ID\n
        Button 1 Label\n
        Button 2 Label\n
        Button 3 Label\n
        Button 1 ID\n
        Button 2 ID\n
        Button 3 ID\n
        '''
        
        self.cursor.execute('''INSERT INTO ticket_system (ticket_message_id, type, guild_id, ticket_channel_id, ticket_category_id, b_one_label, b_two_label, b_three_label, b_one_id, b_two_id, b_three_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                            (ticket_message_id, t_type, guild_id, ticket_channel_id, ticket_category_id, b_one_label, b_two_label, b_three_label, b_one_id, b_two_id, b_three_id,))
        self.db.commit()
        return True


    ##################################################################################################################

    def insert_ticket(self, ticket_id, guild_id, ticket_creator, created_at, members):
        
        self.cursor.execute('INSERT INTO tickets (ticket_id, guild_id, ticket_creator, created_at, members) VALUES (%s, %s, %s, %s, %s)',
                            (ticket_id, guild_id, ticket_creator, created_at, members,))
        self.db.commit()
        return True


    
    ##################################################################################################################
                                                # D E L E T E # 
    ##################################################################################################################

    def delete_case(self, target_id, guild_id, case_id):
        self.cursor.execute('DELETE FROM history WHERE user_id = %s AND guild_id = %s AND case_id = %s', (target_id, guild_id, case_id,))
        self.db.commit()
        return True
    

    def delete_ticket_system(self, guild_id, message_id):
        self.cursor.execute('DELETE FROM ticket_system WHERE guild_id = %s AND ticket_message_id = %s', (guild_id, message_id,))
        self.db.commit()
        return True

    def delete_ticket(self, ticket_id, guild_id):
        self.cursor.execute('DELETE FROM tickets WHERE ticket_id = %s AND guild_id = %s', (ticket_id, guild_id,))
        self.db.commit()
        return True


    ##################################################################################################################
                                                # L E V E L - S Y S T E M # 
    ##################################################################################################################
    
    
    def level_user_query(self, user_id, guild_id):
        '''INSERT: User ID; Guild ID\n\n
        Output:\n
        0. Level Points;\n
        1. Level\n
        2. Last Message XP'''
        self.cursor.execute('SELECT level_points, level, last_msg_xp FROM level_system WHERE user_id = %s AND guild_id = %s', (user_id, guild_id,))
        output = self.cursor.fetchone()

        if output is not None:
            return output
        else:
            output = None
    
    
    def level_insert_new_user(self, user_id, guild_id):
        '''INSERT: User ID; Guild ID'''
        self.cursor.execute('INSERT INTO level_system (user_id, guild_id, level_points) VALUES (%s, %s, %s)', (user_id, guild_id, 0))
        self.db.commit()
        return True
    
    
    def level_user_update(self, level_points, level, last_msg_xp, user_id, guild_id):
        '''
        Input\n
        Update Data -> Level Points | Level | Last Msg XP\n
        Search Date -> User ID | Guild ID'''

        self.cursor.execute('UPDATE level_system SET level_points = %s, level = %s, last_msg_xp = %s WHERE user_id = %s AND guild_id = %s',
                            (level_points, level, last_msg_xp, user_id, guild_id,))
        
        self.db.commit()
        return True
    
    
    
    ##################################################################################################################
                                                # G I V E A W A Y - S Y S T E M # 
    ##################################################################################################################
    
    
    def insert_giveaway(self, giveaway_id, time, prize, channel_id, guild_id, participants, winners, requierement):
        self.cursor.execute('INSERT INTO giveaway (giveaway_id, time, prize, message, channel_id, guild_id, participants, winners, finished, requierement) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                            (giveaway_id, time, prize, None, channel_id, guild_id, participants, winners, 0, requierement,))
        self.db.commit()
        return True
    

    def update_giveaway(self, message_id, guild_id, giveaway_id):
        self.cursor.execute('UPDATE giveaway SET message = %s WHERE guild_id = %s AND giveaway_id = %s', (message_id, guild_id, giveaway_id,))
        self.db.commit()
        return True


    def fetch_giveaway_participants(self, guild_id, giveaway_id):
        self.cursor.execute('SELECT participants FROM giveaway WHERE guild_id = %s AND giveaway_id = %s', (guild_id, giveaway_id,))
        output = self.cursor.fetchone()
        if output is not None:
            return output
        else:
            output = None
    
    def update_giveaway_participants(self, participants, guild_id, giveaway_id):
        self.cursor.execute('UPDATE giveaway SET participants = %s WHERE guild_id = %s AND giveaway_id = %s', (participants, guild_id, giveaway_id,))
        self.db.commit()
        return True
    
    def get_giveaway_ending(self):
        self.cursor.execute('SELECT time, message, guild_id, channel_id, giveaway_id, prize, participants, finished FROM giveaway')
        output = self.cursor.fetchall()
        if output is not None:
            return output
        else:
            output = None
    
    def remove_giveaway(self, giveaway_id, guild_id):
        self.cursor.execute('DELETE FROM giveaway WHERE giveaway_id = %s AND guild_id = %s', (giveaway_id, guild_id,))
        self.db.commit()
        return True
    
    def mark_giveaway_as_finished(self, giveaway_id, finished):
        self.cursor.execute('UPDATE giveaway SET finished = %s WHERE giveaway_id = %s', (finished, giveaway_id,))
        self.db.commit()
        return True
    
    def determine_winners(self, giveaway_id):
        self.cursor.execute('SELECT participants, winners FROM giveaway WHERE giveaway_id = %s', (giveaway_id,))
        output = self.cursor.fetchone()
        if output is not None:
            return output
        else:
            output = None

    def ga_embed_data(self, giveaway_id):
        self.cursor.execute('SELECT b_extra_four FROM buttons WHERE b_extra_three = %s', (giveaway_id,))
        output = self.cursor.fetchone()
        if output is not None:
            return output
        else:
            output = None
            
    def query_giveaway_data(self, giveaway_id):
        '''Output Order\n
        0 = Message\n
        1 = Participants\n
        2 = Channel ID\n
        3 = Prize'''
        
        self.cursor.execute('SELECT message, participants, channel_id, prize FROM giveaway WHERE giveaway_ID = %s', (giveaway_id,))
        output = self.cursor.fetchone()
        if output is not None:
            return output
        else:
            output = None

    ##################################################################################################################
                                            # B U T T O N S - P E R S I S T E N T # 
    ##################################################################################################################
       
    def query_buttons(self, guild_id):
        self.cursor.execute('SELECT b_extra_one, b_extra_two, b_extra_three, b_extra_four, b_extra_five FROM buttons WHERE guild_id = %s', (guild_id,))
        output = self.cursor.fetchone()
        if output is not None:
            return output
        else:
            output = None
            
    def insert_button(self, b_extra_one, b_extra_two, b_extra_three, b_extra_four, b_extra_five, guild_id):
        self.cursor.execute('INSERT INTO buttons (b_extra_one, b_extra_two, b_extra_three, b_extra_four, b_extra_five, guild_id) VALUES (%s, %s, %s, %s, %s, %s)', 
                            (b_extra_one, b_extra_two, b_extra_three, b_extra_four, b_extra_five, guild_id,))
        self.db.commit()
        return True