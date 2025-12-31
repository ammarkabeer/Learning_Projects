#include <iostream>
#include <string>
using namespace std;
//first i made a structure
struct Bankaccount {
    string accnt_holder_name;
     float balance;
    int acccnnumber;
     string acccnt_type;
    float intrst_rate; // applicable only for Savings accounts
};
int accountcapcty= 0;    //this is use for to show initialy it is zero
int accountCount = 0;
Bankaccount* accounts;
//i use this function to resize the account array means number of accounts which i enter in program
void accountarrayresize() {
    if (accountCount >= accountcapcty) {
           //i use Ternary Operator for short method instead of if else
        int newcapcty = (accountcapcty== 0) ? 1 : accountcapcty* 2;
        Bankaccount* newaccnts = new Bankaccount[newcapcty];
        for (int i = 0; i < accountCount; i++) {
            newaccnts[i] = accounts[i];
        }
        delete[] accounts;
        accounts = newaccnts;
        accountcapcty= newcapcty;
    }
}
//this function is use for add new account and store member information
void addnewaccnt() {
   accountarrayresize();
    
    Bankaccount newaccnt;  //acces structure information
    //memeber deatails entry
    cout << "Enter Account Holder Name: ";
    cin >>ws; // name enter
    getline (cin,newaccnt.accnt_holder_name);
    cout<< "Enter Account Number: ";
    cin >> newaccnt.acccnnumber;
    cout << "Enter Initial Balance: ";
    cin >> newaccnt.balance;
    cout << "Enter Account Type (Savings/Checking): ";
    cin >>ws;
    getline (cin, newaccnt.acccnt_type);
    cout<<endl;
   //use this condition to calculte interest rates
    if (newaccnt.acccnt_type == "Savings") {
        cout << "Enter Interest Rate: ";
        cin >> newaccnt.intrst_rate;
    } else {
        newaccnt.intrst_rate = 0.0;
    }
 //this is i use for count number of accounts how many enter there
    accounts[accountCount++] = newaccnt;
    cout << "Account created successfully!" << endl;
}

//this function is used fr deposit money

void depositmoney(int acccnnumber, float amt) {
    //i use a coondition for calculation depsoit money
    for (int i = 0; i < accountCount; i++) {
        if (accounts[i].acccnnumber == acccnnumber) {
            accounts[i].balance += amt;
            cout << "Deposit successful! New balance: $" << accounts[i].balance << endl;
            return;
        }
    }
    //if id not found then this shows
    cout << "Account not found!" << endl;
}

//show account details by its id this function is used for this purpose
void showaccount(int acccnnumber) {
    for (int i = 0; i < accountCount; ++i) {
        //use this condion for check id is availbe or nott
        if (accounts[i].acccnnumber == acccnnumber) {
            //show detail of memebr
            cout << "Account Holder Name: " << accounts[i].accnt_holder_name << endl;
            cout << "Account Number: " << accounts[i].acccnnumber << endl;
            cout << "Balance: $" << accounts[i].balance << endl;
            cout << "Account Type: " << accounts[i].acccnt_type << endl;
            if (accounts[i].acccnt_type == "Savings") {
                cout << "Interest Rate: " << accounts[i].intrst_rate << "%" << endl;
            }
            return;
        }
    }
    //if not availbele then this show
    cout << "Account not found!" << endl;
}
//this function use for calculation of transfer money
void transfermoney(int fromacccnnumber, int toacccnnumber, float amt) {
    int strtindex = -1, endindex = -1;//this is used for indexeschecking 
    for (int i = 0; i < accountCount; i++) {
        if (accounts[i].acccnnumber == fromacccnnumber) {
            strtindex = i;//if accountnumber match theeen start
        }
        if (accounts[i].acccnnumber == toacccnnumber) {
            endindex = i;
        }
    }//use condition for check account index array
    if (strtindex == -1 || endindex == -1) {
        cout << "One or both accounts not found!" << endl;
        return;
    }//calclute money when it add,substraction,or big it
    if (accounts[strtindex].balance >= amt) {
        accounts[strtindex].balance -= amt;
        accounts[endindex].balance += amt;
        cout << "Transfer successful!" << endl;
    } else {//if not balance avilbe
        cout << "Insufficient balance in source account!" << endl;
    }
}
//this function use for money with draw
void moneywithdraw(int acccnnumber, float amt) {
    for (int i = 0; i < accountCount; i++) {
        if (accounts[i].acccnnumber == acccnnumber) {
            //calclute money when it add,substraction,or big it
            if (accounts[i].balance >= amt) {
                accounts[i].balance -= amt;
                cout << "Withdrawal successful! New balance: $" << accounts[i].balance << endl;
            } else {//if not balance avilbe
                cout << "Insufficient balance!" << endl;
            }
            return;
        }
    }
    cout << "Account not found!" << endl;
}

//this function delete account by using backspace method
void deleteaccount(int acccnnumber) { //acesss acctnumber
    for (int i = 0; i < accountCount; i++) {
        //condion checks if account number equals
        if (accounts[i].acccnnumber == acccnnumber) {
            //the loop starts
            for (int j = i; j < accountCount - 1; ++j) {
                accounts[j] = accounts[j + 1];
            }
            accountCount--;//minus 1 account use this
            cout << "Account closed successfully!" << endl;
            return;
        }
    }
    cout << "Account not found!" << endl;
}
//this funnctionc alculate interest 
void calculateinterest() {
    for (int i = 0; i < accountCount; i++) {
        if (accounts[i].acccnt_type == "Savings") {
            float interest = accounts[i].balance * (accounts[i].intrst_rate / 100);//formula to calcluate interest
            accounts[i].balance += interest;
            cout << "Interest added to account " << accounts[i].acccnnumber << ": $" << interest << endl;
        }
    }
}
//thsi function use for show all acoounts which are enter
void showaccounts() {
    //if non account enter the this condition run
    if (accountCount == 0) {
        cout << "No accounts to display." << endl;
        return;
    }
    //if it found accounts then it shows all accounts
    for (int i = 0; i < accountCount; i++) {
        //account holder deatalils
        cout << "Account Holder Name: " << accounts[i].accnt_holder_name << endl;
        cout << "Account Number: " << accounts[i].acccnnumber << endl;
        cout << "Balance: $" << accounts[i].balance << endl;
        cout << "Account Type: " << accounts[i].acccnt_type << endl;//calculation of interests and condition check
        if (accounts[i].acccnt_type == "Savings") {
            cout << "Interest Rate: " << accounts[i].intrst_rate << "%" << endl;
        }
        
    }
}
//main function 
int main() {
    int n;//input n varible
    //use loop to cehck conditions until
    while (true) {
        cout << "1. Create a new account" << endl;
        cout << "2. View account" << endl;
        cout << "3. Deposit money" << endl;
        cout << "4. Withdraw money" << endl;
        cout << "5. Transfer money between accounts" << endl;
        cout << "6. show all accounts" << endl;
        cout << "7. Calculate interest for Savings accounts" << endl;
        cout << "8. Close an account" << endl;
        cout << "9. Exit" << endl;
        cout << "Enter your number choice: ";
        cin >> n;

        int acccnnumber, toacccnnumber;
        float amt; //use switch condition and call functions
        switch (n) {
            case 1:
                addnewaccnt();
                break;
            case 2:
                cout << "Enter your account number: ";
                cin >> acccnnumber;
                showaccount(acccnnumber);
                break;
            case 3:
                cout << "Enter account number: ";
                cin >> acccnnumber;
                cout << "Enter amt to deposit: ";
                cin >> amt;
                depositmoney(acccnnumber, amt);
                break;
            case 4:
                cout << "Enter your account number: ";
                cin >> acccnnumber;
                cout << "Enter amountt you want to withdraw: ";
                cin >> amt;
                moneywithdraw(acccnnumber, amt);
                break;
            case 5:
                cout << "Enter your now account number: ";
                cin >> acccnnumber;
                cout << "Enter yourdestination account number: ";
                cin >> toacccnnumber;
                cout << "Enter amountt which you want to transfer: ";
                cin >> amt;
                transfermoney(acccnnumber, toacccnnumber, amt);
                break;
            case 6:
                showaccounts();
                break;
            case 7:
                calculateinterest();
                break;
            case 8:
                cout << "Enter your account number to close: ";
                cin >> acccnnumber;
               deleteaccount(acccnnumber);
                break;
            case 9:
                cout << "Program Exit" << endl;
                
            default:
                cout << "Invalid n! Please try again." << endl;
        }
        cout << endl;
    }
}