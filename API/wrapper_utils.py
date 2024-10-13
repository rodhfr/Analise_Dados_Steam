# get company string name by game id -------------------

    def fetch_company_names_for_games(self, read_file_path, initial_limit=0, end_limit=0, write_file_path=''):
        all_games_tmp_file = self.all_games_tmp_file  
        tmp_file_exists = self.check_baseline_info()

        if tmp_file_exists:
            games_data = tmp_file_exists
        else:
            print("Baseline file not present, getting info from API...")
            games_data = self.fetch_details_for_all_games(read_file_path, initial_limit, end_limit)

        # Load all_games_tmp_file into a dictionary
        all_games_data = self.load_games_data(all_games_tmp_file)

        company_names = {}
        failed_company_names = [] 
        for game_name, game_data in games_data.items():
            print(game_name)
            game_ids = game_data['id']

            if isinstance(game_ids, int):   
                game_ids_str = str(game_ids) 
            else:
                game_ids_str = ', '.join(map(str, game_ids))

            # Requesting company data for the game
            req_ask = f'fields id, involved_companies.company; where id = ({game_ids_str});'
            game_details = self._make_request(endpoint='games', data=req_ask) 

            if not game_details:
                print(f"No game details returned for game: {game_name}")
                company_names[game_name] = []
            else:
                # Extract involved company IDs from the response
                involved_companies = game_details[0].get('involved_companies', [])
                company_ids = [company['company'] for company in involved_companies]

                if not company_ids:
                    print(f"No companies found for game: {game_name}")
                    company_names[game_name] = []
                    failed_company_names.append(game_name)
                else:
                    # Request company names using the company IDs
                    company_ids_str = ', '.join(map(str, company_ids))
                    company_req = f'fields name; where id = ({company_ids_str});'
                    company_data = self._make_request(endpoint='companies', data=company_req)

                    if not company_data:
                        print(f"No company data returned for game: {game_name}")
                        company_names[game_name] = []
                        failed_company_names.append(game_name)

                    else:
                        company_names[game_name] = [company['name'] for company in company_data]

        # Update all_games_data with company names
        for game_name in all_games_data:
            all_games_data[game_name]['company_names'] = company_names.get(game_name, [])

        # Writing data to file
        self.write_data_to_file(data=all_games_data, output='fetch_company_names_for_games.json')
        if write_file_path:
            self.write_data_to_file(data=all_games_data, output=write_file_path)

        self.write_data_to_file(data=failed_company_names, output='failed_company_games.json')
        return company_names
