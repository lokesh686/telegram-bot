import matplotlib.pyplot as plt

def create_pie_chart(data):
    categories, amounts = zip(*data)
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title("Expense Distribution")
    plt.savefig("report.png")
    plt.close()
