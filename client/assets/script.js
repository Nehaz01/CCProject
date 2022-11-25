
// var base_url = 'http://127.0.0.1:8000';
var base_url = 'http://54.227.174.190:8000';
var x = null;

function getResults() {

    var age = document.querySelector('#age').value;
    var gender = document.querySelector('#gender').value;
    var chest_pain = document.querySelector('#chest_pain').value;
    var bps = document.querySelector('#bps').value;
    var cholesterol = document.querySelector('#cholesterol').value;
    var sugar = document.querySelector('#sugar').value;
    var ecg = document.querySelector('#ecg').value;
    var hr = document.querySelector('#hr').value;
    var angina = document.querySelector('#angina').value;
    var peak = document.querySelector('#peak').value;
    var slope = document.querySelector('#slope').value;

    if(age === '' || gender === '' || chest_pain === '' || bps === '' || cholesterol === '' || sugar === '' || ecg === '' || hr === '' || angina === '' || peak === '' || slope === '') {
        alert('Please enter all values');
        return;
    }

    var postData = {
        'age': age,
        'gender': gender,
        'chest_pain': chest_pain,
        'bps': bps,
        'cholesterol': cholesterol,
        'sugar': sugar,
        'ecg': ecg,
        'hr': hr,
        'angina': angina,
        'peak': peak,
        'slope': slope
    };

    var result_elm = document.querySelector('#result');

    $.post(base_url + "/infer", postData, function(data, status, xhr) {

        x = data;

        if(status === 'success' || data['status']) {

            if(data['has_heart_disease']) {
                var prob = Math.round(data['probability'] * 10000) / 100;

                result_elm.innerHTML = '<span class="text-danger">You have ' + prob + '% chance of having a heart disease.</span>';
            } else {
                result_elm.innerHTML = '<span class="text-success">Congrats! You do not have a heart disease.</span>';
            }

        } else {
            result_elm.innerHTML = 'An error occurred trying to connect to the server.';
        }

        console.log(data);
    });
}

