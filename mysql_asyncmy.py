import os
import asyncmy
import asyncio
from typing import Optional, Any, Tuple, List
import asyncmy.errors



class A_DB:
    def __init__(self):
        self.pool = None

    async def connect(self, maxsize: int = 10):
        self.pool = await asyncmy.create_pool(
            host=os.getenv("HOST"),
            user=os.getenv("MEMBERNAME"),
            password=os.getenv("PASSWORD"),
            db=os.getenv("DATABASE"),
            maxsize=maxsize,
            autocommit=True
        )

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def _execute(self, query: str, params: Optional[Tuple[Any, ...]] = None,
                       fetch: str = "none") -> Optional[Any]:
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, params or ())
                    if fetch == "one":
                        return await cursor.fetchone()
                    elif fetch == "all":
                        return await cursor.fetchall()
        except asyncmy.errors.Error as e:
            print(f"⚠️ DB-Fehler: {e} → Query: {query}")
            return None
        

    async def create_tables(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('''CREATE TABLE IF NOT EXISTS server (
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
                await cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                            case_id  VARCHAR(20) UNIQUE,
                            guild_id BIGINT, 
                            user_id BIGINT, 
                            case_creator BIGINT, 
                            date TIMESTAMP, 
                            reason VARCHAR(255),
                            info VARCHAR(255), 
                            changes LONGTEXT,
                            type TINYTEXT,
                            case_status VARCHAR(255)
                            )''')
                await cursor.execute('''CREATE TABLE IF NOT EXISTS ticket_system (
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
                await cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                            ticket_id BIGINT UNIQUE,
                            guild_id BIGINT,
                            ticket_creator BIGINT, 
                            created_at TIMESTAMP,
                            members VARCHAR(255)
                            )''')
                await cursor.execute('''CREATE TABLE IF NOT EXISTS dashboard_sessions (
                            session_id VARCHAR(20) UNIQUE,
                            token TEXT,
                            refresh_token TEXT,
                            token_expires_at TIMESTAMP,
                            user_id TEXT)''')
                await cursor.execute('''CREATE TABLE IF NOT EXISTS level_system (
                            user_id BIGINT,
                            guild_id BIGINT,
                            level_points BIGINT,
                            level BIGINT,
                            last_msg_xp TIMESTAMP)''')
                await cursor.execute('''CREATE TABLE IF NOT EXISTS giveaway (
                            giveaway_id INTEGER,
                            time BIGINT,
                            prize TEXT,
                            message BIGINT,
                            channel_id BIGINT,
                            guild_id BIGINT,
                            participants TEXT,
                            winners INTEGER,
                            finished BOOL,
                            requierement VARCHAR(25),
                            value VARCHAR(1500))''')
                await cursor.execute('''CREATE TABLE IF NOT EXISTS buttons (
                                b_extra_one VARCHAR(50),
                                b_extra_two VARCHAR(50),
                                b_extra_three VARCHAR(50),
                                b_extra_four VARCHAR(1000),
                                b_extra_five VARCHAR(50),
                                guild_id BIGINT)''')
           

    ##################################################################################################################
                                                # Q U E R Y # 
    ##################################################################################################################

    async def query_server_table(self, guild_id):
        
        '''Input Guild ID\n\n
        
        Output Order
        0 = Guild ID\n
        1 = Admin Role ID\n
        2 = Moderator Role ID\n
        3 = Supporter Role ID\n
        4 = Global Channel ID\n
        5 = Language\n
        6 = VIP'''
        
        query = ('SELECT guild_id, admin_role, moderator_role, supporter_role, global_channel, language, vip FROM server WHERE guild_id = %s')
        result = await self._execute(query, (guild_id,), fetch="one")
        return result
    
    #----------------------------------------------------------------------------------------------------------------#
    
    async def query_all_global_channels(self):
        query = ('SELECT global_channel FROM server')
        result = await self._execute(query, fetch="all")
        return result
    
    #----------------------------------------------------------------------------------------------------------------#
    
    async def query_custom_one_slot(self, user_in, d_b, search_value):
            query = f'SELECT {user_in} FROM {d_b} WHERE guild_id = %s'
            return await self._execute(query, (search_value,), fetch="one")

    #----------------------------------------------------------------------------------------------------------------#
    
    async def query_all_case_ids(self, member_id, guild_id):
        query = 'SELECT case_id FROM history WHERE user_id = %s AND guild_id = %s'
        return await self._execute(query, (member_id, guild_id), fetch="all")

    #----------------------------------------------------------------------------------------------------------------#

    async def query_all_case_ids_with_type(self, member_id, guild_id, c_type):
        query = 'SELECT case_id FROM history WHERE user_id = %s AND guild_id = %s AND type = %s'
        return await self._execute(query, (member_id, guild_id, c_type), fetch="all")
    
    #----------------------------------------------------------------------------------------------------------------#

    async def query_case_reason_and_type(self, case_id, guild_id):
        query = 'SELECT info, type FROM history WHERE case_id = %s AND guild_id = %s'
        return await self._execute(query, (case_id, guild_id), fetch="one")
    
    #----------------------------------------------------------------------------------------------------------------#

    async def query_case_all(self, case_id, guild_id):
        query = ('SELECT case_creator, date, reason, info, changes, type, case_status '
                 'FROM history WHERE case_id = %s AND guild_id = %s')
        return await self._execute(query, (case_id, guild_id), fetch="one")
    
    #----------------------------------------------------------------------------------------------------------------#
    
    async def query_case_with_user(self, target_id, guild_id, case_id):
        
        '''Input -> Member ID | Guild ID | Case ID\n\n
        
        Output Order:\n
        0 = Case Creator\n
        1 = Date\n
        2 = Reason\n
        3 = Info\n
        4 = Changes\n
        5 = Type\n
        6 = Case Status'''
        
        query = ('SELECT case_creator, date, reason, info, changes, type, case_status '
                 'FROM history WHERE case_id = %s AND guild_id = %s')
        return await self._execute(query, (case_id, guild_id), fetch="one")

    #----------------------------------------------------------------------------------------------------------------#
    
    async def query_all_cases_via_case_id_with_offset(self, offset_count, target_id, guild_id):
        limit = 25
        offset = limit * offset_count
        query = (f'SELECT case_id, type FROM moderation WHERE user_id = %s AND guild_id = %s '
                 f'LIMIT {limit} OFFSET {offset}')
        return await self._execute(query, (target_id, guild_id), fetch="all")

    #----------------------------------------------------------------------------------------------------------------#
    
    async def query_case_informations(self, target_id, guild_id, case_id):
        query = ('SELECT warned_by, reason, date, last_edit_time, last_edit_by FROM moderation '
                 'WHERE user_id = %s AND guild_id = %s AND case_id = %s')
        return await self._execute(query, (target_id, guild_id, case_id), fetch="one")

    #----------------------------------------------------------------------------------------------------------------#
    
    async def query_ticket_informations(self, ticket_id):
        '''
        Input Order -> Ticket ID\n\n
        Output Order:\n
        0 = Ticket Creator ID\n
        1 = Created at\n
        2 = Members
        '''
        query = ('SELECT ticket_creator, created_at, members FROM tickets WHERE ticket_id = %s')
        return await self._execute(query, (ticket_id,), fetch="one")

    #----------------------------------------------------------------------------------------------------------------#
    
    async def query_ticket_system(self, guild_id):
        '''
        Input -> Guild ID\n\n
        
        Output Order:\n
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
        10 = Button 3 ID
        '''
        query = ('SELECT ticket_message_id, type, guild_id, ticket_channel_id, ticket_category_id, b_one_label, b_two_label, b_three_label, b_one_id, b_two_id, b_three_id '
                 'FROM ticket_system WHERE guild_id = %s')
        return await self._execute(query, (guild_id,), fetch="one")

    #----------------------------------------------------------------------------------------------------------------#
    
    async def query_tickets_by_user(self, guild_id, user_id):
        
        '''Input Order -> Guild ID | Ticket Creator ID'''
        
        query = ('SELECT ticket_id FROM tickets WHERE guild_id = %s AND ticket_creator = %s')
        return await self._execute(query, (guild_id, user_id), fetch="all")

    #----------------------------------------------------------------------------------------------------------------#
        
    
    
    
    
    ##################################################################################################################
                                                # U P D A T E # 
    ##################################################################################################################


    async def update_custom_one_slot(self, t, u_para, update_value, guild_id):
        query = (f'UPDATE {t} SET {u_para} = %s WHERE guild_id = %s')
        await self._execute(query, (update_value, guild_id))
        return True

    #----------------------------------------------------------------------------------------------------------------#
    
    async def update_administrator_role(self, role_id, guild_id):
        query = ("UPDATE server SET admin_role = %s WHERE guild_id = %s")
        await self._execute(query, (role_id, guild_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def update_moderator_role(self, role_id, guild_id):
        query = ("UPDATE server SET moderator_role = %s WHERE guild_id = %s")
        await self._execute(query, (role_id, guild_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def update_supporter_role(self, role_id, guild_id):
        query = ("UPDATE server SET supporter_role = %s WHERE guild_id = %s")
        await self._execute(query, (role_id, guild_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def update_language(self, language, guild_id):
        query = ("UPDATE server SET language = %s WHERE guild_id = %s")
        await self._execute(query, (language, guild_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def update_global_channel(self, global_channel, guild_id):
        query = ("UPDATE server SET global_channel = %s WHERE guild_id = %s")
        await self._execute(query, (global_channel, guild_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def update_case_reason(self, reason, edit_at, edit_by, case_id, guild_id):
        query = (
            "UPDATE moderation SET reason = %s, last_edit_time = %s, last_edit_by = %s "
            "WHERE case_id = %s AND guild_id = %s")
        await self._execute(query, (reason, edit_at, edit_by, case_id, guild_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def update_case(self, reason, changes, case_id, guild_id):
        query = ("UPDATE history SET reason = %s, changes = %s WHERE case_id = %s AND guild_id = %s")
        await self._execute(query, (reason, changes, case_id, guild_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def update_case_status(self, case_status, guild_id, case_id):
        query = ("UPDATE history SET case_status = %s WHERE guild_id = %s AND case_id = %s")
        await self._execute(query, (case_status, guild_id, case_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def update_ticket_system_after_create(self, ticket_channel, ticket_category, b_one_id, b_two_id, b_three_id, guild_id):
        query = (
            "UPDATE ticket_system SET ticket_channel_id = %s, ticket_category_id = %s, "
            "b_one_id = %s, b_two_id = %s, b_three_id = %s WHERE guild_id = %s")
        await self._execute(query, (ticket_channel, ticket_category, b_one_id, b_two_id, b_three_id, guild_id))
        return True

    #----------------------------------------------------------------------------------------------------------------#
    
    
    
    
    
    ##################################################################################################################
                                                # I N S E R T # 
    ##################################################################################################################
    
    async def insert_custom_one_slot(self, table, update_parameter, guild_id, update_value):
        # ⚠️ Sicherheitsprüfung empfohlen für table und update_parameter
        query = (f'INSERT INTO {table} (guild_id, {update_parameter}) VALUES (%s, %s)')
        await self._execute(query, (guild_id, update_value))
        return True

    #----------------------------------------------------------------------------------------------------------------#

    async def insert_administrator_role(self, guild_id, role_id):
        query = ('INSERT INTO server (guild_id, admin_role) VALUES (%s, %s)')
        await self._execute(query, (guild_id, role_id))
        return True

    #----------------------------------------------------------------------------------------------------------------#

    async def insert_moderator_role(self, guild_id, role_id):
        query = ('INSERT INTO server (guild_id, moderator_role) VALUES (%s, %s)')
        await self._execute(query, (guild_id, role_id))
        return True

    #----------------------------------------------------------------------------------------------------------------#

    async def insert_supporter_role(self, guild_id, role_id):
        query = ('INSERT INTO server (guild_id, supporter_role) VALUES (%s, %s)')
        await self._execute(query, (guild_id, role_id))
        return True

    #----------------------------------------------------------------------------------------------------------------#

    async def insert_language(self, guild_id, language):
        query = ('INSERT INTO server (guild_id, language) VALUES (%s, %s)')
        await self._execute(query, (guild_id, language))
        return True

    #----------------------------------------------------------------------------------------------------------------#

    async def insert_case(self, guild_id, member_id, moderator_id, current_time, reason, info, random_id, entry_type, case_status):
        
        '''Input Order:\n
        Guild ID | Member ID | Moderator ID | Date | Reason | Info | Case ID | Type | Case Status'''
        
        query = ('INSERT INTO history (guild_id, user_id, case_creator, date, reason, info, case_id, type, case_status) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
        await self._execute(query, (guild_id, member_id, moderator_id, current_time, reason, info, random_id, entry_type, case_status))
        return True

    #----------------------------------------------------------------------------------------------------------------#

    async def insert_ticket_system(self, ticket_message_id, t_type, guild_id, ticket_channel_id, ticket_category_id,
                                b_one_label, b_two_label, b_three_label, b_one_id, b_two_id, b_three_id):
        '''
        Input Order:\n
        Ticket Message ID | Ticket Type | Guild ID | Channel ID | Category ID |
        Button 1 Label | Button 2 Label | Button 3 Label |
        Button 1 ID | Button 2 ID | Button 3 ID
        '''
        query = ('INSERT INTO ticket_system (ticket_message_id, type, guild_id, ticket_channel_id, ticket_category_id, '
                'b_one_label, b_two_label, b_three_label, b_one_id, b_two_id, b_three_id) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
        await self._execute(query, (
            ticket_message_id, t_type, guild_id, ticket_channel_id, ticket_category_id,
            b_one_label, b_two_label, b_three_label, b_one_id, b_two_id, b_three_id
        ))
        return True

    #----------------------------------------------------------------------------------------------------------------#

    async def insert_ticket(self, ticket_id, guild_id, ticket_creator, created_at, members):
        query = ('INSERT INTO tickets (ticket_id, guild_id, ticket_creator, created_at, members) '
                'VALUES (%s, %s, %s, %s, %s)')
        await self._execute(query, (ticket_id, guild_id, ticket_creator, created_at, members))
        return True

    #----------------------------------------------------------------------------------------------------------------#





    ##################################################################################################################
                                            # B U T T O N S - P E R S I S T E N T # 
    ##################################################################################################################
       

    async def query_buttons(self, guild_id):
        query = (
            'SELECT b_extra_one, b_extra_two, b_extra_three, b_extra_four, b_extra_five, guild_id '
            'FROM buttons WHERE guild_id = %s')
        return await self._execute(query, (guild_id,), fetch="all")
    
    #----------------------------------------------------------------------------------------------------------------#

    async def insert_button(self, b_extra_one, b_extra_two, b_extra_three, b_extra_four, b_extra_five, guild_id):
        query = (
            'INSERT INTO buttons (b_extra_one, b_extra_two, b_extra_three, b_extra_four, b_extra_five, guild_id) '
            'VALUES (%s, %s, %s, %s, %s, %s)')
        await self._execute(query, (b_extra_one, b_extra_two, b_extra_three, b_extra_four, b_extra_five, guild_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#
    
    
    
    
    
    ##################################################################################################################
                                                # G I V E A W A Y - S Y S T E M # 
    ##################################################################################################################
    

    async def insert_giveaway(self, giveaway_id, time, prize, channel_id, guild_id, participants, winners, requierement, value):
        query = (
            'INSERT INTO giveaway (giveaway_id, time, prize, message, channel_id, guild_id, participants, '
            'winners, finished, requierement, value) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
        await self._execute(query, (
            giveaway_id, time, prize, None, channel_id, guild_id,
            participants, winners, 0, requierement, value))
        return True

    #----------------------------------------------------------------------------------------------------------------#

    async def update_giveaway(self, message_id, guild_id, giveaway_id):
        query = ('UPDATE giveaway SET message = %s WHERE guild_id = %s AND giveaway_id = %s')
        await self._execute(query, (message_id, guild_id, giveaway_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def fetch_giveaway_participants(self, guild_id, giveaway_id):
        query = ('SELECT participants FROM giveaway WHERE guild_id = %s AND giveaway_id = %s')
        return await self._execute(query, (guild_id, giveaway_id), fetch="one")
    
    #----------------------------------------------------------------------------------------------------------------#

    async def update_giveaway_participants(self, participants, guild_id, giveaway_id):
        query = ('UPDATE giveaway SET participants = %s WHERE guild_id = %s AND giveaway_id = %s')
        await self._execute(query, (participants, guild_id, giveaway_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def get_giveaway_ending(self):
        query = ('SELECT time, message, guild_id, channel_id, giveaway_id, prize, participants, finished FROM giveaway')
        return await self._execute(query, fetch="all")
    
    #----------------------------------------------------------------------------------------------------------------#

    async def remove_giveaway(self, giveaway_id, guild_id):
        query = ('DELETE FROM giveaway WHERE giveaway_id = %s AND guild_id = %s')
        await self._execute(query, (giveaway_id, guild_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def mark_giveaway_as_finished(self, giveaway_id, finished):
        query = ('UPDATE giveaway SET finished = %s WHERE giveaway_id = %s')
        await self._execute(query, (finished, giveaway_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def determine_winners(self, giveaway_id):
        query = ('SELECT participants, winners FROM giveaway WHERE giveaway_id = %s')
        return await self._execute(query, (giveaway_id,), fetch="one")

    #----------------------------------------------------------------------------------------------------------------#
    
    async def ga_embed_data(self, giveaway_id):
        query = ('SELECT b_extra_four FROM buttons WHERE b_extra_three = %s')
        return await self._execute(query, (giveaway_id,), fetch="one")
    
    #----------------------------------------------------------------------------------------------------------------#

    async def query_giveaway_data(self, giveaway_id):
        
        '''
        Output Order:\n
        0 = Message\n
        1 = Participants\n
        2 = Channel ID\n
        3 = Prize\n
        4 = Requirement\n
        5 = Value
        '''
        
        query = (
            'SELECT message, participants, channel_id, prize, requierement, value '
            'FROM giveaway WHERE giveaway_id = %s')
        return await self._execute(query, (giveaway_id,), fetch="one")
    
    #----------------------------------------------------------------------------------------------------------------#
    
    
    


    ##################################################################################################################
                                                # L E V E L - S Y S T E M # 
    ##################################################################################################################
    

    async def level_user_query(self, user_id, guild_id):
        
        '''
        Input:\n
        Member ID | Guild ID\n\n

        Output:\n
        0. Level Points\n
        1. Level\n
        2. Last Message XP
        '''
        
        query = ('SELECT level_points, level, last_msg_xp FROM level_system WHERE user_id = %s AND guild_id = %s')
        return await self._execute(query, (user_id, guild_id), fetch="one")
    
    #----------------------------------------------------------------------------------------------------------------#

    async def level_insert_new_user(self, user_id, guild_id):
        query = ('INSERT INTO level_system (user_id, guild_id, level_points) VALUES (%s, %s, %s)')
        await self._execute(query, (user_id, guild_id, 0))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def level_user_update(self, level_points, level, last_msg_xp, user_id, guild_id):
        '''
        Update Data:\n
        Level Points | Level | Last MSG XP\n\n

        Where:\n
        - MEMBER ID | Guild ID
        '''
        query = ('''
            UPDATE level_system
            SET level_points = %s, level = %s, last_msg_xp = %s
            WHERE user_id = %s AND guild_id = %s''')
        await self._execute(query, (level_points, level, last_msg_xp, user_id, guild_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#
    
    
    
    
    
    ##################################################################################################################
                                                # D E L E T E # 
    ##################################################################################################################


    async def delete_case(self, target_id, guild_id, case_id):
        query = ('DELETE FROM history WHERE user_id = %s AND guild_id = %s AND case_id = %s')
        await self._execute(query, (target_id, guild_id, case_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def delete_ticket_system(self, guild_id, message_id):
        query = ('DELETE FROM ticket_system WHERE guild_id = %s AND ticket_message_id = %s')
        await self._execute(query, (guild_id, message_id))
        return True
    
    #----------------------------------------------------------------------------------------------------------------#

    async def delete_ticket(self, ticket_id, guild_id):
        query = ('DELETE FROM tickets WHERE ticket_id = %s AND guild_id = %s')
        await self._execute(query, (ticket_id, guild_id))
        return True

    