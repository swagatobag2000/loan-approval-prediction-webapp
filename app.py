from flask import Flask, escape, request, render_template
import pickle

app = Flask("Loan prediction")
model = pickle.load(open('model.bin', 'rb'))


@app.route('/')
def home():
    return render_template("index.html")
    # return "Pinging model"


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # gender
        if (gender == "Male"):
            gender_val = 1
        else:
            gender_val = 0

        # married
        if(married == "Yes"):
            married_val = 1
        else:
            married_val = 0

        # dependents
        if(dependents == '1'):
            dependents_val = 1
        elif(dependents == '2'):
            dependents_val = 2
        elif(dependents == "3+"):
            dependents_val = 3
        else:
            dependents_val = 0

        # education
        if (education == "Not Graduate"):
            education_val = 1
        else:
            education_val = 0

        # employed
        if (employed == "Yes"):
            employed_val = 1
        else:
            employed_val = 0

        # property area

        if(area == "Semiurban"):
            area_val = 1
        elif(area == "Urban"):
            area_val = 2
        else:
            area_val = 0

        totalincome = ApplicantIncome+CoapplicantIncome

        prediction = model.predict([[ApplicantIncome, LoanAmount, Loan_Amount_Term, credit, totalincome,
                                     gender_val, married_val, dependents_val, education_val, employed_val, area_val]])

        # print(prediction)

        if(prediction == "N"):
            prediction = "Rejected"
        else:
            prediction = "Approved"

        return render_template("prediction.html", prediction_text="Your Loan status is {}".format(prediction))

    else:
        return render_template("prediction.html")


if __name__ == "__main__":
    app.run(debug=True)
