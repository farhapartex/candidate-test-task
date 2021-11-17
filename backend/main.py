import pandas as pd
import os


class CSVParser:
    """
    A class responsible for reading and parsing csv files from the
    crypto wallets and exchanges.
    """

    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.transactions = []
        self._process_df()

    def _process_df(self):
        """
        This private method is responsible to fill null value in csv, set a proper name in columns and to check is there
        one amount column or not
        """
        new_columns = {}
        for col in self.df.columns.values:
            if col.lower() in ["date", "date time", "time"]:
                new_columns[col] = "date"
            elif col.lower() in ["currency", "currencies"]:
                new_columns[col] = "currency"
            else:
                new_columns[col] = col.lower()

        self.df.rename(columns=new_columns, inplace=True)
        self.has_amount_col = True if "amount" in self.df.columns.values else False

        for col in self.df.columns.values:
            if "amount" in col:
                self.df[col] = self.df[col].fillna(0).astype(float)

    def _process_transactions(self):
        """
        This private method is responsible to fetch date, transaction type, amount information and store them in a list
        """
        columns = self.df.columns.values

        trade_has_prev_transaction = False

        for index, row in self.df.iterrows():
            transaction = {
                'date': None,
                'transaction_type': None,
                'received_amount': None,
                'received_currency_iso': None,
                'sent_amount': None,
                'sent_currency_iso': None,
            }
            if "date" in columns:
                transaction["date"] = row["date"]

            if "type" in columns:
                if row["type"].lower() in ["trade", "buy", "sell"]:
                    transaction["transaction_type"] = "Trade"
                else:
                    transaction["transaction_type"] = row["type"].lower().title()

            if transaction["transaction_type"] == "Trade":
                if self.has_amount_col:
                    if trade_has_prev_transaction:
                        transaction = self.transactions[-1]
                    if row["amount"] < 0:
                        transaction["sent_amount"] = (-1) * row["amount"]
                        transaction["sent_currency_iso"] = row["currency"]
                    else:
                        transaction["received_amount"] = row["amount"]
                        transaction["received_currency_iso"] = row["currency"]

                    if trade_has_prev_transaction:
                        trade_has_prev_transaction = False
                        continue
                    else:
                        trade_has_prev_transaction = True
                else:
                    currencies = row["currency"].split("-")
                    transaction["sent_amount"] = row["sold amount"]
                    transaction["sent_currency_iso"] = currencies[0]
                    transaction["received_amount"] = row["bought amount"]
                    transaction["received_currency_iso"] = currencies[2]

            elif transaction["transaction_type"] == "Withdrawal":
                """
                Process data for Withdrawal
                """
                transaction = self._get_deposit_or_withdraw_data(type="Withdrawal", transaction=transaction, row=row)
            elif transaction["transaction_type"] == "Deposit":
                """
                Process data for Deposit
                """
                transaction = self._get_deposit_or_withdraw_data(type="Deposit", transaction=transaction, row=row)

            self.transactions.append(transaction)

    def _get_deposit_or_withdraw_data(self, type: str, transaction: dict, row: pd.Series) -> dict:
        transaction["sent_amount"] = None if type == "Deposit" else 0
        transaction["sent_currency_iso"] = None if type == "Deposit" else ""
        transaction["received_amount"] = None if type == "Withdrawal" else 0
        transaction["received_currency_iso"] = None if type == "Withdrawal" else ""

        if type == "Withdrawal":
            dict_amount_key = "sent_amount"
            dict_currency_key = "sent_currency_iso"
            df_amount_col = "amount" if self.has_amount_col else "sold amount"
        else:
            dict_amount_key = "received_amount"
            dict_currency_key = "received_currency_iso"
            df_amount_col = "amount" if self.has_amount_col else "bought amount"

        transaction[dict_amount_key] = abs(row[df_amount_col])
        transaction[dict_currency_key] = row["currency"]

        return transaction

    def get_json_results(self) -> list:
        self._process_transactions()
        return self.transactions

    def print_results(self):
        """
        Public method printing the output from parsing transactions
        """
        print(self.get_json_results())


if __name__ == '__main__':
    #parser = CSVParser('exchange_files/exchange_1_transaction_file.csv')
    #parser = CSVParser('exchange_files/exchange_2_transaction_file.csv')
    #print(parser.get_json_results())
    # parser.print_results()
    pass