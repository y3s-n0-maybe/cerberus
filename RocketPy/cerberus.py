from rocketpy import Environment, SolidMotor, Rocket, Flight, Parachute, NoseCone, TrapezoidalFins, RailButtons, Function, Tail

import datetime, math

curves_dir = "cerberus\\RocketPy\\curves\\"
sustainer_thrust = curves_dir + "thrust two.rse"
sustainer_drag = curves_dir + "drag two.csv"
booster_thrust = curves_dir + "thrust one.rse"
booster_drag = curves_dir + "drag one.csv"

booster_burnout = 1.7
sustainer_delay = 2

sustainer_radius = 0.048
booster_radius = 0.0565

total_length = 3.2
sustainer_length = 2.1
nose_length = 0.504

booster_motor_length = 0.404
booster_motor_dry_mass = .650
booster_motor_total_mass = 1.632
booster_motor_giir = 0.00725
booster_motor_or = 0.027
booster_motor_grain_number = 5
booster_motor_grain_density = (booster_motor_total_mass - booster_motor_dry_mass) / ((booster_motor_length * math.pi * booster_motor_or**2) - (booster_motor_length * math.pi * booster_motor_giir**2))
booster_xy_inertia = (1/12 * booster_motor_dry_mass * (3 * (booster_motor_or ** 2) + (booster_motor_length ** 2)))
booster_tensor = [booster_xy_inertia, booster_xy_inertia, (.5 * booster_motor_dry_mass * booster_motor_or)]

sustainer_motor_length = 0.5
sustainer_motor_dry_mass = .641
sustainer_motor_total_mass = 1.632
sustainer_motor_giir = 0.001
sustainer_motor_or = 0.027
sustainer_motor_grain_number = 5
sustainer_motor_grain_density = (sustainer_motor_total_mass - sustainer_motor_dry_mass) / ((sustainer_motor_length * math.pi * sustainer_motor_or**2) - (sustainer_motor_length * math.pi * sustainer_motor_giir**2))
sustainer_xy_inertia = (1/12 * sustainer_motor_dry_mass * (3 * (sustainer_motor_or ** 2) + (sustainer_motor_length ** 2)))
sustainer_tensor = [sustainer_xy_inertia, sustainer_xy_inertia, (.5 * sustainer_motor_dry_mass * sustainer_motor_or)]

varDate = datetime.datetime(2026, 7, 1, hour = 12)

env =  Environment(latitude = 55.435108, longitude = -5.691520, date = varDate)
env.set_atmospheric_model(type = "Windy", file = "ICON") 

def prints():
    print("Stage One \n")
    booster_flight.prints.all()
    print("Stage Two \n")
    sustainer_flight.prints.all()

    print("Drift Distance: ", drift)

    print("\nAtmospheric Model")
    env.prints.atmospheric_conditions()

def plot_traj():
    booster_flight.plots.trajectory_3d()
    sustainer_flight.plots.trajectory_3d()

def draw():
    booster.draw(vis_args=None, plane='xz', filename=None)
    sustainer.draw(vis_args=None, plane='xz', filename=None)

def plot_all():
    booster_flight.plots.all()
    sustainer_flight.plots.all()

def drag_sep():
    booster_height = booster_flight.get_solution_at_time(booster_burnout + sustainer_delay)[3]
    sustainer_height = sustainer_flight.get_solution_at_time(booster_burnout + sustainer_delay)[3]
    print("Booster Height: ", booster_height, "\nSustainer Height: ", sustainer_height,"\nDistance at Ignition: ", sustainer_height - booster_height)

booster_motor = SolidMotor(
    coordinate_system_orientation = "nozzle_to_combustion_chamber",
    center_of_dry_mass_position = booster_motor_length / 2,
    dry_inertia = sustainer_tensor,
    dry_mass = booster_motor_dry_mass,
    grain_density = booster_motor_grain_density,
    grain_initial_height = booster_motor_length / booster_motor_grain_number,
    grain_initial_inner_radius = booster_motor_giir,
    grain_number = booster_motor_grain_number,
    grain_outer_radius = booster_motor_or,
    grain_separation = 0,
    grains_center_of_mass_position = booster_motor_length / 2,
    nozzle_radius = .01,
    thrust_source = booster_thrust
    )   

sustainer_motor = SolidMotor(
    coordinate_system_orientation = "nozzle_to_combustion_chamber",
    center_of_dry_mass_position = sustainer_motor_length / 2,
    dry_inertia = booster_tensor,
    dry_mass = sustainer_motor_dry_mass,
    grain_density = sustainer_motor_grain_density,
    grain_initial_height = sustainer_motor_length / sustainer_motor_grain_number,
    grain_initial_inner_radius = sustainer_motor_giir,
    grain_number = sustainer_motor_grain_number,
    grain_outer_radius = sustainer_motor_or,
    grain_separation = 0,
    grains_center_of_mass_position = sustainer_motor_length / 2,
    nozzle_radius = 0.01,
    thrust_source = sustainer_thrust
    )

booster = Rocket(
    center_of_mass_without_motor = total_length - 1.83,
    coordinate_system_orientation = "tail_to_nose",
    power_off_drag = booster_drag,
    power_on_drag = booster_drag,
    inertia = [0.71, 0.71, 0.015],
    mass = 9.143,
    radius = sustainer_radius

)

sustainer = Rocket(
    center_of_mass_without_motor = 0.94,
    coordinate_system_orientation = "tail_to_nose",
    power_off_drag = sustainer_drag,
    power_on_drag = sustainer_drag,
    inertia = [1.75, 1.75, 0.01],
    mass = 3.162,
    radius = sustainer_radius
)

transition = Tail(
    length = 0.09,
    top_radius =  sustainer_radius,
    bottom_radius = booster_radius,
    rocket_radius = booster_radius,
    name = "Transgender"
)

booster.add_motor(booster_motor, position = 0)

sustainer.add_motor(sustainer_motor, position = 0)

booster.add_parachute(
    name = "Booster Chute",
    cd_s = 0.36482938495,
    trigger = "apogee",
    sampling_rate = 1,
    lag = 5
    )

booster.add_trapezoidal_fins(
    cant_angle = 0.0,
    name = "Stage One Fins",
    n = 4,
    root_chord = 0.16,
    span = 0.09,
    sweep_length = 0.025,
    tip_chord = 0.15,
    position = .2
)

sustainer_fins = TrapezoidalFins(
    cant_angle = 0.0,
    name = "Sustainer Fins",
    n = 4,
    root_chord = 0.13,
    span = 0.08,
    sweep_length = 0.025,
    tip_chord = 0.11,
    rocket_radius = sustainer_radius,
)

nose = NoseCone (
    base_radius  = sustainer_radius,
    rocket_radius = sustainer_radius,
    kind  =  "ogive",
    length  = nose_length,
    name  =  "Nose Cone Two",
)

booster.add_surfaces([transition, nose, sustainer_fins], [1.095, total_length, total_length-1.9])

sustainer.add_parachute(
    name = "Sustainer Main", 
    cd_s = 0.524894787288,
    trigger = 300,
    sampling_rate = 1,
    lag = 0
    )

sustainer.add_parachute(
    name = "drogue", 
    cd_s = 0.23379732528,
    trigger = "apogee",
    sampling_rate = 5
    )

sustainer.add_surfaces([nose, sustainer_fins], [sustainer_length, .2])

"""booster.set_rail_buttons(
    lower_button_position =  0.9266,
    angular_position = 45,
    upper_button_position = 0.6266
)"""

booster_flight = Flight(
    rocket = booster,
    environment = env,
    rail_length = 2.0,
    inclination = 90,
    
    verbose = True
)

sustainer_flight = Flight(
    rocket = sustainer,
    environment = env,
    rail_length = 2,
    heading = env.wind_direction(15),
    inclination = 85,
    initial_solution = booster_flight.get_solution_at_time(booster_burnout),
    verbose = True
)

solution = sustainer_flight.get_solution_at_time(200, 50)
x = float(solution[1])
y = float(solution[2])
drift = math.sqrt(math.pow(x, 2) + math.pow(y, 2))

# Print flight conditions 

drag_sep()
prints()
plot_traj()
draw()
#plot_all()