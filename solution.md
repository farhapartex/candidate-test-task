## How I design the solution

### Before design and write algorithm lets have a look to the problem and corner cases

There are some (this problem has two file but it can have more then two) crypto currency transactions csv files which need to parse and get data as list of json. The core parts of the problem are:

* There are mainly three types of transactions, which are Deposit, Withdrawal and Trade
* A Trade can be denoted as Trade/Buy/Sell
* A single transaction information can be described in one row or two row in the csv file
* There could be different column name for same data, Example: Amount/Sold Amount/ Buy Amount/ Date/ Time/ Date Time etc. Also there can be typo issue
* Since all file structure may not be same, and we have to return data in a specific format hence it is important to justify data in such a way that when which one will assign to which key

### Solution algorithm

* First need to pre process the DataFrame which can be found by using Pandas. 
    * Fetch all columns from the DataFrame
    * Loop over the column values list and do the following
        * Changed column value to lower case and check if the name is like date/time/date time, if yes rename it as only `date`
        * Changed column value to lower case and check if the name is like currency/currencies, rename it to `currency`
        * Else just lower case it
        * In the list of columns check that, if there is any column with only name `amount`, if has set `True` to a variable `has_amount_col` else `False`. If there is column with `amount` it means that some transaction may need two rows and it is a flag for us.
    * Take a empty list named as `transactions` where we will append each transaction dictionary with proper value
    * Loop over the rows of DataFrame and for each row take a dictionary named as transaction with some default value:
        * keep the date in transaction
        * Take the type column and check the value
            * If the value are one of those `trade`/`buy`/`sell`, then set the type as `Trade` else keep the type as title(First letter is capital)
            * If the transactio type is `Trade`
                * First check if `has_amount_col` is `True` or `False`. If it is `True` means single transaction occured more than one row, hence we will use a flag `trade_has_prev_transaction`.
                * If `has_amount_col` is False  we will take proper data from this row and will assign to the transaction dictionary
                * If `has_amount_col` is True and `trade_has_prev_transaction` is False then:
                    * Check if the amount is positive or negetive. If positive, means it is value of receieve amount else sent amount
                    * Store the absolute value of amount in the transaction dictionary
                * If `has_amount_col` is True and `trade_has_prev_transaction` is True then:
                    * Take the last appended transaction dictionary from transaction list and update amount value as positive or negetive
            * If the transaction type is `Deposit`
                * there will be no sent amount and set it `None` also to the sent currency
                * there will be only recieve amount and recieve currency
            * If the transaction type is `Withdrawal`
                * there will be no recieve amount and recieve currency
                * there will be only sent amount and sent currency
            * append the transaction dictionary in the `transactions` list

## Backend


### CSVParser class

Let's have a look to its methods

* `_process_df` this private method do some pre process work on the dataframe, found from a csv
* `_process_transactions` this private method process each row of the dataframe and generate the transaction dictionary and store it in the `transactions` list
* `_get_deposit_or_withdraw_data` this private method is responsible to process transaction dictionary for `Deposit` or `Withdrawal` type transaction
* `get_json_results` this public method return a the list of all transactions
* `print_results` this public method use `get_json_results` method to print the transactions list


### API

* Since we have to show data in frontend we need a minimal backend API hence I used Flask and created a simple API which:
    * First fetch all csv files from the `exchange_files` folder
    * For each file it use the `CSVParser` class to get the transaction list by using the `get_json_results` public method and append the result to a final list.
    * After looping all files , it return the final list to user/frontend


## Frontend

* In frontend I use vuejs and created component named as `TransactionList`, `Table` and `Cell`
* I used bootstrep css framework for styling
* I used `axios` packages to fetch data from the API call


### Project Setup

* Open your terminal and navigate to backend folder
* Create a virtual environment, turn it on and install all packages from requirements.txt file
* Run ther server by this command `flask run`
* Open another terminal and navigate to `frontend` folder
* Run `yarn` command to install packages
* Run `yarn serve` to start frontend server