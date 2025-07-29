from django.shortcuts import render


def bmi_calculator(request):
    bmi = None
    message = None
    weight = None
    height = None
    weight_unit = None
    height_unit = None
 
    if request.method == 'POST':
        try:
            # Get data from the form
            weight = float(request.POST.get('weight'))
            weight_unit = request.POST.get('weight_unit')
            height = float(request.POST.get('height'))
            height_unit = request.POST.get('height_unit')

            # Convert weight to kilograms
            if weight_unit == 'lbs':
                weight *= 0.453592  # 1 lb = 0.453592 kg

            # Convert height to meters for BMI calculation
            if height_unit == 'cm':
                height_in_meters = height / 100  # 1 meter = 100 cm
            elif height_unit == 'ft':
                height_in_meters = height * 0.3048  # 1 foot = 0.3048 meters
            else:
                height_in_meters = height  # assume height is already in meters

            # Calculate BMI: weight (kg) / (height (m))^2
            if height_in_meters > 0:  # Ensure height is not zero to prevent division by zero error
                bmi = weight / (height_in_meters ** 2)
                bmi = round(bmi, 2)  # Round BMI to 2 decimal places

                # Determine BMI category
                if bmi < 18.5:
                    message = "Underweight"
                elif 18.5 <= bmi < 24.9:
                    message = "Normal weight"
                elif 24.9 <= bmi < 29.9:
                    message = "Overweight"
                else:
                    message = "Obese"
            else:
                message = "Height cannot be zero or negative."

        except (ValueError, TypeError):
            message = "Invalid input. Please enter valid numbers for weight and height."
        except Exception as e:
            message = f"An unexpected error occurred: {e}"

    context = {
        'bmi': bmi,
        'message': message,
        'weight': weight,
        'height': height,
        'weight_unit': weight_unit,
        'height_unit': height_unit,
    }
    return render(request, 'tools/bmi_calculator.html', context)  # Make sure the correct template is used












from django.shortcuts import render

def calorie_calculator(request):
    if request.method == 'POST':
        try:
            # Get form data
            age = float(request.POST.get('age'))
            gender = request.POST.get('gender')
            weight = float(request.POST.get('weight'))
            height = float(request.POST.get('height'))
            activity_level = request.POST.get('activity_level')
            weight_unit = request.POST.get('weight_unit')  # kg or lbs
            height_unit = request.POST.get('height_unit')  # cm or feet

            # Convert weight if in pounds
            if weight_unit == 'lbs':
                weight = weight * 0.453592  # Convert lbs to kg

            # Convert height if in feet (and inches)
            if height_unit == 'ft_inch':
                feet = int(height)  # Feet part
                inches = (height - feet) * 12  # Extract decimal part for inches
                height_in_cm = (feet * 30.48) + (inches * 2.54)  # Convert feet and inches to cm
                height = height_in_cm
            elif height_unit == 'cm':
                height = height  # No conversion needed for cm

            # Calculate BMR using Mifflin-St Jeor formula
            if gender == 'male':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5  # BMR for men
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161  # BMR for women

            # Activity factor
            activity_factor = {
                'sedentary': 1.2,
                'light': 1.375,
                'moderate': 1.55,
                'active': 1.725
            }.get(activity_level, 1.2)

            # Calculate daily calories
            daily_calories = bmr * activity_factor

            return render(request, 'tools/calorie_calculator.html', {
                'daily_calories': daily_calories,
                'age': age,
                'gender': gender,
                'weight': weight,
                'height': round(height, 2),
                'activity_level': activity_level,
                'weight_unit': weight_unit,
                'height_unit': 'cm',  # Always show in cm after conversion
            })
        except ValueError:
            message = "Invalid input, please try again."
            return render(request, 'tools/calorie_calculator.html', {'message': message})

    return render(request, 'tools/calorie_calculator.html', {})
