let hours = new Date().getHours();

let greeting;

if (6 <= hours && hours < 12)
    greeting = 'Доброе утро';
else if (12 <= hours && hours < 18)
    greeting = 'Добрый день';
else if (18 <= hours && hours < 24)
    greeting = 'Добрый вечер';
else
    greeting = 'Доброй ночи';

let greetWho = document.getElementById('greeting').innerHTML;
document.getElementById('greeting').innerHTML = greeting + ', ' + greetWho + '!';
