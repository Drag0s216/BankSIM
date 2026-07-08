import json, random

class BankAccount():
    def __init__(self,  uid=None):
        self.uid = uid


    def logs(self, uid, transType, amount):
        logList = []

        try:
            with open("TransactionLogs.json", 'r') as f:
                logList = json.load(f)
        except Exception as e:
            print("Log File NOT Found. Creating...")

        nr = random.randint(10000, 100000)
        while any(str(nr) in log for log in logList):
            nr = random.randint(10000, 100000)
        
        payload = {
            f"{nr}":{   
                f"{uid}": {
                "transType": f"{transType}",
                "amount": f"{amount}"
                }
            }
        }

        logList.append(payload)

        with open("TransactionLogs.json", "w") as f:
            f.write(json.dumps(logList, indent=4))
        

    def accCheck(self):

        accList = []

        try:
            with open("Accounts.json", "r") as f:
                accList = json.load(f)

                for account in accList:
                    if str(self.uid) in account:
                        accountData = account[str(self.uid)]
            
                        f.close()
                        return True, accountData
                    
                return False, None
                    
        except Exception as e:
            #print(e)
            return False, None

    def accInfo(self):
        account = self.accCheck()
        if account[0]:
            print(account[1])

        else:
            pass

    interest = 0
    overdraftLimit = 0

    def registerAcc(self):
        self.uid = random.randrange(1000, 10000)
        fName = input("First Name: ")
        lName = input("Last Name: ")

        accountType = input("Account Type (C/S): ")
        while (accountType.upper() != 'C') and (accountType.upper() != "S"):
            accountType = input("Account Type (C/S): ")

        while True:
            try:
                age = int(input("Age: "))
                break
            except Exception as e: print("Invalid age input!\n", e)

        while True:
            try:
                initialSold = float(input("Amount to Deposit: "))
                break
            except Exception as e: print("Invalid age input!\n", e)
        

        try:
            with open("Accounts.json", 'r') as f:
                accList = json.load(f)

        except:
            print("\nDatabase not found! Creating...")
            accList = []


        while self.accCheck()[0]:
            self.uid = random.randrange(1000, 10000)
    
        payload = {
            f"{self.uid}": {
                "fName": fName,
                "lName": lName,
                "age": age,
                "sold": initialSold,
                "interest": self.interest,
                "overdraftLimit": self.overdraftLimit,
                "accountType": accountType.upper()
            },
        }

        accList.append(payload)

        with open("Accounts.json", 'w') as f:
            f.write(json.dumps(accList, indent=4))
            f.close()

        print(f"Account Registered!\nUID: {self.uid}\n")

    def deposit(self):
        if self.accCheck()[0]:
            while True:
                try:
                    amount = float(input("Amount to deposit: "))
                    break
                except Exception as e: print("Invalid Operation\n", e)
            
            accList = []

            
            with open("Accounts.json", "r") as f:
                accList = json.load(f)

                for account in accList:
                    if str(self.uid) in account:
                        account[str(self.uid)]['sold'] = float(account[str(self.uid)]['sold']) + amount
                        print(f"Operation Sucessful!\nAccount Sold: {account[str(self.uid)]['sold']}")


            with open("Accounts.json", 'w') as f:
                f.write(json.dumps(accList, indent=4))
                f.close()

            self.logs(self.uid, "Deposit", amount)

        else: print("Account NOT Found!")

    def withdraw(self):
        account = self.accCheck()
        accList = []

        if account[0]:

            while True:
                try:
                    amount = float(input("Amount to withdraw: "))
                    break
                except Exception as e: print("Invalid Operation\n", e)
            
            updatedSold = float(account[1]["sold"]) - amount


            with open("Accounts.json", "r") as f:
                accList = json.load(f)

            for account in accList:
                if str(self.uid) in account:
                    if updatedSold <= -self.overdraftLimit:
                        print("Overdraft Exceeded! Withdrawal Rejected!")
                        
                    else:
                        account[str(self.uid)]['sold'] = float(account[str(self.uid)]['sold']) - amount

                        with open("Accounts.json", 'w') as f:
                            f.write(json.dumps(accList, indent=4))
                            f.close()
                        
                        print(f"Successful Operation. Account sold: {updatedSold}")

                        self.logs(self.uid, "Withdraw", amount)
        
        else: print("Account NOT Found!")

    def transfer(self):
        sender = self.accCheck()
        accList = []


        if sender[0]:
            while True:
                try:
                    transferUid = int(input("Transfer UID: "))
                    break
                except Exception as e:
                    print(f"Invalid Operation!\n{e}")

            receiver = BankAccount(transferUid).accCheck()
            

            if receiver[0]:
                while True:
                    try:
                        amount = float(input("Amount to Transfer: "))
                        break
                    except Exception as e:
                        print(f"Invalid Operation!\n{e}")

                updatedSold = float(sender[1]['sold']) - amount

                with open("Accounts.json", 'r') as f:
                    accList = json.load(f)

                for account in accList:
                    if str(self.uid) in account:
                        if updatedSold <= -self.overdraftLimit:
                            print("Overdraft Exceeded! Transfer Rejected!")
                            return
                            
                        
                        else:
                            account[str(self.uid)]['sold'] = float(account[str(self.uid)]['sold']) - amount
                
                for account in accList:
                    if str(transferUid) in account:
                        account[str(transferUid)]['sold'] = float(account[str(transferUid)]['sold']) + amount
                
                with open("Accounts.json", 'w') as f:
                    f.write(json.dumps(accList, indent=4))
                    f.close()
                
                print("Money Transfered Successfully!")

                self.logs(self.uid, "Transfer", amount)

                        
            else: print("Receiver Account NOT Found!")
        else: print("Sender Account NOT Found!")



class SavingsAccount(BankAccount):
    interest = 10
    overdraftLimit = 0




class CurrentAccount(BankAccount):
    interest = 0
    overdraftLimit = 500


def login(uid):
    accountData = BankAccount(uid).accCheck()[1]["accountType"]

    if accountData == "S":
        account = SavingsAccount(uid)
    else:
        account = CurrentAccount(uid)


    while True:
        print("\n1. Account Info")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Logout")

        prompt = input("Choose an Option: ")

        match prompt:
            case "1":
                account.accInfo()
            case "2":
                account.deposit()
            case "3":
                account.withdraw()
            case "4":
                account.transfer()
            case "5":
                return
            case _:
                print("Invalid Operation!\n")

            

def main():
    while True:
        print("1. Register\n2. Login\n3. Exit")
        
        startPrompt = input("Choose an Option: ")

        match startPrompt:
            case "1":
                BankAccount().registerAcc()
            case "2":
                uid = input("Account UID: ")
                account = BankAccount(uid).accCheck()
                if account[0]:
                    login(uid)

                else:
                    print("Account NOT Found!\n")
            case "3":
                exit(1)
            case _:
                print("Invalid Operation\n")

if __name__ == "__main__":
    main()