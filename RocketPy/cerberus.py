# For most up to date code: check github https://www.github.com/y3s-n0-maybe/cerberus

from rocketpy import Environment, SolidMotor, Rocket, Flight, Parachute, NoseCone, TrapezoidalFins, RailButtons, Function, Tail

import datetime, math, matplotlib.pyplot as plt, rocketpy.tools as tls, numpy as np

curves_dir = "C:\\Users\\Owner\\Desktop\\Rockets\\cerberus\\RocketPy\\curves\\"
sustainer_thrust = curves_dir + "thrust two.rse"
sustainer_drag = curves_dir + "drag two.csv"
booster_thrust = curves_dir + "thrust one.rse"
booster_drag = curves_dir + "drag one.csv"

booster_burnout = 1.7
sustainer_delay = 2

sustainer_radius = 0.096/2
booster_radius = 0.113/2

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
sustainer_motor_total_mass = 1.654
sustainer_motor_giir = 0.001
sustainer_motor_or = 0.027
sustainer_motor_grain_number = 5
sustainer_motor_grain_density = (sustainer_motor_total_mass - sustainer_motor_dry_mass) / ((sustainer_motor_length * math.pi * sustainer_motor_or**2) - (sustainer_motor_length * math.pi * sustainer_motor_giir**2))
sustainer_xy_inertia = (1/12 * sustainer_motor_dry_mass * (3 * (sustainer_motor_or ** 2) + (sustainer_motor_length ** 2)))
sustainer_tensor = [sustainer_xy_inertia, sustainer_xy_inertia, (.5 * sustainer_motor_dry_mass * sustainer_motor_or)]

varDate = datetime.datetime(2026, 7, 1, hour = 12)

env =  Environment(latitude = 55.435108, longitude = -5.691520, date = varDate)
env.set_atmospheric_model(type = "Windy", file = "ICON") 

#env.set_atmospheric_model(type="custom_atmosphere", pressure=None, temperature=300, wind_u=[ (15, 8), (1000, 6) ], wind_v=[ (15, 0), (1000, 4.5) ], )

def kinematics(self, *, filename=None):  # pylint: disable=too-many-statements
    """Prints out all Kinematics graphs available about the Flight

    Parameters
    ----------
    filename : str | None, optional
        The path the plot should be saved to. By default None, in which case
        the plot will be shown instead of saved. Supported file endings are:
        eps, jpg, jpeg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff
        and webp (these are the formats supported by matplotlib).

    Returns
    -------
    None
    """
    ax4 = plt.subplot()
    ax4.plot(self.speed[:, 0], self.speed[:, 1], color="#ff7f0e")
    ax4.set_xlim(0, self.t_final)
    ax4.set_title("Velocity Magnitude | Acceleration Magnitude")
    ax4.set_xlabel("Time (s)")
    ax4.set_ylabel("Velocity (m/s)", color="#ff7f0e")
    ax4.tick_params("y", colors="#ff7f0e")
    ax4.grid(True)

    ax4up = ax4.twinx()
    ax4up.plot(
        self.acceleration[:, 0],
        self.acceleration[:, 1],
        color="#1f77b4",
    )
    ax4up.set_ylabel("Acceleration (m/s²)", color="#1f77b4")
    ax4up.tick_params("y", colors="#1f77b4")

    plt.show()

def aerodynamics(self, *, filename=None):  # pylint: disable=too-many-statements
    """Prints out all Forces and Moments graphs available about the Flight

    Parameters
    ----------
    filename : str | None, optional
        The path the plot should be saved to. By default None, in which case
        the plot will be shown instead of saved. Supported file endings are:
        eps, jpg, jpeg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff
        and webp (these are the formats supported by matplotlib).

    Returns
    -------
    None
    """

    ax1 = plt.subplot()
    ax1.plot(
        self.aerodynamic_lift[: tls.find_closest(self.time_steps, self.apogee_time), 0],
        self.aerodynamic_lift[: tls.find_closest(self.time_steps, self.apogee_time), 1],
        label="Resultant",
    )
    ax1.plot(
        self.R1[: tls.find_closest(self.time_steps, self.apogee_time), 0],
        self.R1[: tls.find_closest(self.time_steps, self.apogee_time), 1],
        label="R1",
    )
    ax1.plot(
        self.R2[: tls.find_closest(self.time_steps, self.apogee_time), 0],
        self.R2[: tls.find_closest(self.time_steps, self.apogee_time), 1],
        label="R2",
    )
    ax1.set_xlim(0, self.apogee_time)
    ax1.set_ylim(0, 3)
    ax1.legend()
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Lift Force (N)")
    ax1.set_title("Aerodynamic Lift Resultant Force")
    ax1.grid()
    plt.show()

    ax2 = plt.subplot()
    ax2.plot(
        self.aerodynamic_drag[: tls.find_closest(self.time_steps, self.apogee_time), 0],
        self.aerodynamic_drag[: tls.find_closest(self.time_steps, self.apogee_time), 1],
    )
    ax2.set_xlim(0, self.apogee_time)
    ax2.set_ylim(0, 200)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Drag Force (N)")
    ax2.set_title("Aerodynamic Drag Force")
    ax2.grid()
    plt.show()

    ax3 = plt.subplot()
    ax3.plot(
        self.aerodynamic_bending_moment[: tls.find_closest(self.time_steps, self.apogee_time), 0],
        self.aerodynamic_bending_moment[: tls.find_closest(self.time_steps, self.apogee_time), 1],
        label="Resultant",
    )
    ax3.plot(
        self.M1[: tls.find_closest(self.time_steps, self.apogee_time), 0],
        self.M1[: tls.find_closest(self.time_steps, self.apogee_time), 1],
        label="M1",
    )
    ax3.plot(
        self.M2[: tls.find_closest(self.time_steps, self.apogee_time), 0],
        self.M2[: tls.find_closest(self.time_steps, self.apogee_time), 1],
        label="M2",
    )
    ax3.set_xlim(0, self.apogee_time)
    ax3.legend()
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Bending Moment (N m)")
    ax3.set_title("Aerodynamic Bending Resultant Moment")
    ax3.grid()
    plt.show()

    ax4 = plt.subplot()
    ax4.plot(
        self.aerodynamic_spin_moment[: tls.find_closest(self.time_steps, self.apogee_time), 0],
        self.aerodynamic_spin_moment[: tls.find_closest(self.time_steps, self.apogee_time), 1],
    )
    ax4.set_xlim(0, self.apogee_time)
    ax4.set_xlabel("Time (s)")
    ax4.set_ylabel("Spin Moment (N m)")
    ax4.set_title("Aerodynamic Spin Moment")
    ax4.grid()
    plt.show()

def fluid_mechanics(self, *, filename=None):  # pylint: disable=too-many-statements
    """Prints out a summary of the Fluid Mechanics graphs available about
    the Flight

    Parameters
    ----------
    filename : str | None, optional
        The path the plot should be saved to. By default None, in which case
        the plot will be shown instead of saved. Supported file endings are:
        eps, jpg, jpeg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff
        and webp (these are the formats supported by matplotlib).

    Returns
    -------
    None
    """
    plt.figure(figsize=(9, 16))

    ax1 = plt.subplot()
    ax1.plot(self.mach_number[:, 0], self.mach_number[:, 1])
    ax1.set_xlim(0, self.t_final)
    ax1.set_title("Mach Number")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Mach Number")
    ax1.grid()
    plt.show()

    ax2 = plt.subplot()
    ax2.plot(self.reynolds_number[:, 0], self.reynolds_number[:, 1])
    ax2.set_xlim(0, self.t_final)
    ax2.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    ax2.set_title("Reynolds Number")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Reynolds Number")
    ax2.grid()
    ax2.plot()
    plt.show()

    ax3 = plt.subplot()
    ax3.plot(
        self.dynamic_pressure[:, 0],
        self.dynamic_pressure[:, 1],
        label="Dynamic Pressure",
    )
    ax3.plot(
        self.total_pressure[:, 0],
        self.total_pressure[:, 1],
        label="Total Pressure",
    )
    ax3.plot(
        self.pressure[:, 0],
        self.pressure[:, 1],
        label="Static Pressure",
    )
    ax3.set_xlim(0, self.t_final)
    ax3.legend()
    ax3.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    ax3.set_title("Total and Dynamic Pressure")
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Pressure (Pa)")
    ax3.grid()
    ax3.plot()
    plt.show()

    ax4 = plt.subplot()
    ax4.plot(self.angle_of_attack[:, 0], self.angle_of_attack[:, 1])
    ax4.set_title("Angle of Attack")
    ax4.set_xlabel("Time (s)")
    ax4.set_ylabel("Angle of Attack (°)")
    ax4.set_xlim(self.out_of_rail_time, self.apogee_time)
    ax4.set_ylim(0, self.angle_of_attack(self.out_of_rail_time))
    ax4.grid()
    ax4.plot()
    plt.show()

    ax5 = plt.subplot()
    ax5.plot(
        self.partial_angle_of_attack[:, 0],
        self.partial_angle_of_attack[:, 1],
    )
    ax5.set_title("Partial Angle of Attack")
    ax5.set_xlabel("Time (s)")
    ax5.set_ylabel("Partial Angle of Attack (°)")
    ax5.set_xlim(self.out_of_rail_time, self.apogee_time)
    ax5.set_ylim(
        0, self.partial_angle_of_attack(self.out_of_rail_time)
    )
    ax5.grid()
    ax5.plot()
    plt.show()

    ax6 = plt.subplot()
    ax6.plot(
        self.angle_of_sideslip[:, 0], self.angle_of_sideslip[:, 1]
    )
    ax6.set_title("Angle of Sideslip")
    ax6.set_xlabel("Time (s)")
    ax6.set_ylabel("Angle of Sideslip (°)")
    ax6.set_xlim(self.out_of_rail_time, self.apogee_time)
    ax6.set_ylim(
        0, self.angle_of_sideslip(self.out_of_rail_time)
    )
    ax6.grid()
    ax6.plot()
    plt.show()

    plt.subplots_adjust(hspace=0.5)

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
    print("Booster Height: ", booster_height, "\nSustainer Height: ", sustainer_height,"\nDistance at Ignition: ", sustainer_height - booster_height, "\n")

def aerodynamics_plots():
    aerodynamics(booster_flight)
    aerodynamics(sustainer_flight)

def fluid_mechanics_plots():
    fluid_mechanics(booster_flight)
    fluid_mechanics(sustainer_flight)

def kinematics_plots():
    kinematics(booster_flight)
    kinematics(sustainer_flight)

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
    center_of_mass_without_motor = total_length - 1.75,
    coordinate_system_orientation = "tail_to_nose",
    power_off_drag = booster_drag,
    power_on_drag = booster_drag,
    inertia = [0.71, 0.71, 0.015],
    mass = 9.985 + sustainer_motor_total_mass,
    radius = booster_radius

)

sustainer = Rocket(
    center_of_mass_without_motor = sustainer_length - 1.21,
    coordinate_system_orientation = "tail_to_nose",
    power_off_drag = sustainer_drag,
    power_on_drag = sustainer_drag,
    inertia = [1.75, 1.75, 0.01],
    mass = 6.288,
    radius = sustainer_radius
)

transition = Tail(
    length = 0.095,
    top_radius =  sustainer_radius,
    bottom_radius = booster_radius,
    rocket_radius = booster_radius,
    name = "Transgender"
)

booster.add_motor(booster_motor, position = 0)

sustainer.add_motor(sustainer_motor, position = 0)

booster.add_parachute(
    name = "Booster Chute",
    cd_s = 0.8 * 3.1415926 * ((.762/2)**2),
    trigger = "apogee",
    sampling_rate = 1,
    lag = 5
    )

booster.add_trapezoidal_fins(
    cant_angle = 0.0,
    name = "Stage One Fins",
    n = 4,
    root_chord = 0.16,
    span = 0.08,
    sweep_length = 0.0252,
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
    cd_s = 0.8 * 3.1415926 * ((.914/2)**2),
    trigger = 300,
    sampling_rate = 1,
    lag = 0
    )

sustainer.add_parachute(
    name = "drogue", 
    cd_s = 0.8 * 3.1415926 * ((.61/2)**2),
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
    heading = round(env.wind_direction(20)),
    
    verbose = True
)

sustainer_flight = Flight(
    rocket = sustainer,
    environment = env,
    rail_length = 2,
    heading = 0,
    inclination = 90,
    initial_solution = booster_flight.get_solution_at_time(booster_burnout),
    verbose = True
)

solution = sustainer_flight.get_solution_at_time(200, 50)
x = float(solution[1])
y = float(solution[2])
drift = math.sqrt(math.pow(x, 2) + math.pow(y, 2))

# Print flight conditions 

#drag_sep()
prints()
#plot_traj()
#draw()
#plot_all()

# Print Seperated Plots

#aerodynamics_plots()
#fluid_mechanics_plots()
#kinematics_plots()