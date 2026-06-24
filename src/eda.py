from data_loader import load_data
data = load_data("data/")

app = data["app"]
bureau = data["bureau"]
prev = data["prev"]

print(app.info())
print(bureau.info())
print(prev.info())
