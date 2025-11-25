import pickle

# A fake simple "model" — just a Python dict
model = {
    "name": "CYBER-DEF25 Dummy Model",
    "version": "1.0",
    "threshold": 0.5
}

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("model.pkl created!")
