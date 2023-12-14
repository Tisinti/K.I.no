document.addEventListener("DOMContentLoaded", function() {
    const calendar = document.querySelector('.calendar');
    const calendarButton = document.getElementById('calendarButton');
    const monthPicker = calendar.querySelector('#month-picker');
    const yearElement = calendar.querySelector('#year');
    const calendarDays = document.querySelectorAll('.calendar-days div');
    const monthList = calendar.querySelector('.month-list');

    calendarButton.addEventListener('click', toggleCalendar);

    function toggleCalendar() {
        const displayStyle = window.getComputedStyle(calendar).display;
        calendar.style.display = (displayStyle === 'none') ? 'block' : 'none';

        const outputArea = document.getElementById('outputArea');
        outputArea.style.display = 'none';
    }

    let selectedDate = null;

    function storeSelectedDate(event) {
        const selectedDay = event.target.textContent.trim();
        const selectedMonth = monthPicker.textContent.trim();
        const selectedYear = yearElement.textContent.trim();

        selectedDate = `${selectedDay}.${selectedMonth}.${selectedYear}`;
        console.log(selectedDate); //Ausgabe Datum Variable (Format: DD.MM.JJJJ): selectedDate

        calendar.style.display = 'none';

        const outputArea = document.getElementById('outputArea');
        outputArea.style.display = 'block';
    
        calendar.style.display = 'none';
    }

    calendarDays.forEach(day => {
        day.addEventListener('click', storeSelectedDate);
    });

    document.addEventListener('click', function(event) {
        if (event.target !== calendarButton && !calendar.contains(event.target)) {
            calendar.style.display = 'none';
        }
    });

    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

    const isLeapYear = (year) => {
        return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
    };

    const getFebDays = (year) => {
        return isLeapYear(year) ? 29 : 28;
    };

    const generateCalendar = (month, year) => {
        const calendarDays = calendar.querySelector('.calendar-days');
        const calendarHeaderYear = calendar.querySelector('#year');

        calendarDays.innerHTML = '';

        const currentDate = new Date();
        if (month === undefined) month = currentDate.getMonth();
        if (year === undefined) year = currentDate.getFullYear();

        const currMonth = `${monthNames[month]}`;
        monthPicker.innerHTML = currMonth;
        calendarHeaderYear.innerHTML = year;

        const daysOfMonth = [31, getFebDays(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        const firstDay = new Date(year, month, 1);

        for (let i = 0; i <= daysOfMonth[month] + firstDay.getDay() - 1; i++) {
            const day = document.createElement('div');
            if (i >= firstDay.getDay()) {
                day.classList.add('calendar-day-hover');
                day.innerHTML = i - firstDay.getDay() + 1;
                day.innerHTML += `<span></span><span></span><span></span><span></span>`;
                if (i - firstDay.getDay() + 1 === currentDate.getDate() && year === currentDate.getFullYear() && month === currentDate.getMonth()) {
                    day.classList.add('curr-date');
                }
                day.addEventListener('click', storeSelectedDate);
            }
            calendarDays.appendChild(day);
        }
    };

    monthNames.forEach((monthName, index) => {
        const month = document.createElement('div');
        month.innerHTML = `<div data-month="${index}">${monthName}</div>`;
        month.querySelector('div').addEventListener('click', () => {
            monthList.classList.remove('show');
            generateCalendar(index, parseInt(yearElement.textContent));
        });
        monthList.appendChild(month);
    });

    monthPicker.addEventListener('click', () => {
        monthList.classList.add('show');
    });

    const currDate = new Date();
    const currMonth = currDate.getMonth();
    const currYear = currDate.getFullYear();

    generateCalendar(currMonth, currYear);

    document.querySelector('#prev-year').addEventListener('click', () => {
        yearElement.textContent = parseInt(yearElement.textContent) - 1;
        generateCalendar(currMonth, parseInt(yearElement.textContent));
    });

    document.querySelector('#next-year').addEventListener('click', () => {
        yearElement.textContent = parseInt(yearElement.textContent) + 1;
        generateCalendar(currMonth, parseInt(yearElement.textContent));
    });
});