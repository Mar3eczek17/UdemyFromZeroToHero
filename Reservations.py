from datetime import datetime, timedelta


class ReservationSystem:
    def __init__(self):
        self.reservations = {}  # empty dictionary to store reservations

    def __add__(self, other):
        self.make_reservation()

    def __del__(self):
        self.cancel_reservation()

    def _get_name(self) -> str:
        name = input("What's your name? ")
        if name.isalpha():
            return name.rstrip()
        # Can use regex ?
        else:
            return self._get_name()

    def _get_reservation_time(self) -> datetime:
        reservation_time = input("When would you like to book? (DD.MM.YYYY HH:MM) ")
        self.reservation_time = datetime.strptime(reservation_time, "%d.%m.%Y %H:%M")
        return self.reservation_time

    def _check_resrvation_time(self, date: datetime):
        # check if the date is less than 1 hour from now
        if reservation_time < datetime.now() + timedelta(hours=1):
            print("Reservation time should be at least 1 hour from now.")

    def make_reservation(self):
        name = self._get_name()
        reservation_time = self._reservation_time()

        # check if the user has more than 2 reservations already this week
        reservations_this_week = [r for r in self.reservations.values() if
                                  r['name'] == name and r['start_time'].isocalendar()[1] ==
                                  reservation_time.isocalendar()[1]]
        if len(reservations_this_week) >= 2:
            print("You cannot have more than 2 reservations this week.")
            return

        # check if the court is already reserved for the time user specified
        reservation_date = reservation_time.strftime("%d.%m.%Y")
        if reservation_date in self.reservations:
            for r in self.reservations[reservation_date]:
                if r['start_time'] <= reservation_time < r['end_time']:
                    print(
                        f"The court is already reserved from {r['start_time'].strftime('%H:%M')} to"
                        f" {r['end_time'].strftime('%H:%M')}.")
                    suggest_reservation_time = r['end_time'] + timedelta(minutes=30)
                    suggest_reservation_time = suggest_reservation_time.replace(second=0, microsecond=0)
                    make_suggestion = input(
                        f"Would you like to make a reservation for {suggest_reservation_time.strftime('%H:%M')} "
                        f"instead? (yes/no) ")
                    if make_suggestion.lower() == "yes":
                        reservation_time = suggest_reservation_time
                    else:
                        return

        # display possible periods in 30 minute intervals up to 90 minutes
        start_time = reservation_time.replace(minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(minutes=90)
        available_periods = []
        for i in range(1, 4):
            if start_time + timedelta(minutes=30 * i) <= end_time:
                available_periods.append(
                    f"{i}) {start_time.strftime('%H:%M')} - {(start_time + timedelta(minutes=30 * i)).strftime('%H:%M')}")
        print("How long would you like to book court?")
        print("\n".join(available_periods))
        choice = input("Enter your choice (1-3): ")
        while not choice.isdigit() or int(choice) not in range(1, 4):
            choice = input("Invalid choice. Enter your choice (1-3): ")
        duration = int(choice) * 30

        # add the reservation to the dictionary
        if reservation_date not in self.reservations:
            self.reservations[reservation_date] = []
        self.reservations[reservation_date].append({
            'name': name,
            'start_time': reservation_time,
            'end_time': reservation_time + timedelta(minutes=duration)
        })
        print(
            f"Reservation made for {name} on {reservation_time.strftime('%d.%m.%Y')} from {reservation_time.strftime('%H:%M')} to {(reservation_time + timedelta(minutes=duration)).strftime('%H:%M')}.")
        # cheack
        print(self.reservations)

    def cancel_reservation(self):
        print("Cancel a reservation")
        name = input("What's your name? ")
        reservation_time = input("When was your reservation? (DD.MM.YYYY HH:MM) ")

        # check if the date is less than 1 hour from now
        if reservation_time < datetime.now() + timedelta(hours=1):
            print("You cannot cancel a reservation less than 1 hour from now.")
            return

        # check if the reservation exists
        reservation_date = reservation_time.strftime("%d.%m.%Y")
        if reservation_date not in self.reservations:
            print(f"No reservations found for {reservation_date}.")
            return
        reservation_exists = False
        for r in self.reservations[reservation_date]:
            if r['name'] == name and r['start_time'] == reservation_time:
                reservation_exists = True
                break
        if not reservation_exists:
            print(
                f"No reservations found for {name} at {reservation_time.strftime('%H:%M')} on {reservation_date}.")
            return

        # remove the reservation
        self.reservations[reservation_date] = [r for r in self.reservations[reservation_date] if
                                               not (r['name'] == name and r['start_time'] == reservation_time)]
        print(f"Reservation for {name} at {reservation_time.strftime('%H:%M')} on {reservation_date} cancelled.")
        # check
        print(self.reservations)


# example usage
rs = ReservationSystem()
rs.make_reservation()
rs.cancel_reservation()
