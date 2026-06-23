import pandas as pd

def load_data(data_path: str) -> dict:
    app = pd.read_csv(f'{data_path}application_train.csv')
    bureau = pd.read_csv(f'{data_path}bureau.csv')
    prev = pd.read_csv(f'{data_path}previous_application.csv')

    print(f"App: {app.shape}")
    print(f"Bureau: {bureau.shape}")
    print(f"Prev: {prev.shape}")
    print(app['TARGET'].value_counts())

    return{
        'app': app,
        'bureau': bureau,
        'prev': prev
    }

if __name__ =='__main__':
    load_data('data/')


    
