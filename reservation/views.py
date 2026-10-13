from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Flight, Booking
from .forms import UserRegistrationForm

def home(request):
    flights = Flight.objects.all()
    return render(request, 'home.html', {'flights': flights})

def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    return render(request, 'flight_detail.html', {'flight': flight})

@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)

    if request.method == 'POST':
        seats_requested = int(request.POST.get('seats', 1))
        if seats_requested <= 0:
            messages.error(request, "Invalid number of seats requested.")
            return redirect('flight_detail', flight_id=flight_id)
        if seats_requested > flight.available_seats:
            messages.error(request, "Not enough seats available.")
            return redirect('flight_detail', flight_id=flight_id)

        # Create booking; the Booking model handles decrementing flight.available_seats
        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            seats_booked=seats_requested
        )

        return render(request, 'confirm_booking.html', {'booking': booking})

    return render(request, 'book_flight.html', {'flight': flight})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_time')
    return render(request, 'my_bookings.html', {'bookings': bookings})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    return render(request, 'confirm_booking.html', {'booking': booking})

