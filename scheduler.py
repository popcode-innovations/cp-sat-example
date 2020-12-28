from ortools.sat.python import cp_model


def main():
    
    tasks_dict = {
      0: {
        'name': 'Yoga',
        'no_of_days': 2,
        'duration': 4
      },
      1: {
        'name': 'Cycling',
        'no_of_days': 2,
        'duration': 4
      },
      2: {
        'name': 'Sales Call',
        'no_of_days': 7,
        'duration': 1
      },
      3: {
        'name': 'Break Fast',
        'no_of_days': 7,
        'duration': 1
      },
      4: {
        'name': 'Work',
        'no_of_days': 5,
        'duration': 1
      },
      5: {
        'name': 'Call Home',
        'no_of_days': 7,
        'duration': 1
      },
      6: {
        'name': 'Lunch',
        'no_of_days': 7,
        'duration': 1
      },
      7: {
        'name': 'Chill Break',
        'no_of_days': 7,
        'duration': 1
      },
      8: {
        'name': 'Meet Arun',
        'no_of_days': 1,
        'duration': 1
      },
      9: {
        'name': 'Watch Netflix',
        'no_of_days': 7,
        'duration': 1
      },
      10: {
        'name': 'Hobby Project',
        'no_of_days': 7,
        'duration': 1
      }
    }

    total_time_per_day = 8

    tasks_info = []

    for x in tasks_dict:
      print (x,':',tasks_dict[x])
      tasks_info.append([x, tasks_dict[x]['no_of_days']])

    no_of_schedules = 8
    no_of_days = 7
    no_of_tasks = len(tasks_dict)

    all_tasks = range(no_of_tasks)
    all_days = range(no_of_days)
    all_schdules = range(no_of_schedules)

    model = cp_model.CpModel()

    tasks = {}

    for n in all_tasks:
      for d in all_days:
        for s in all_schdules:
          tasks[(n, d,
            s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    #C1: There should not be multiple tasks at the same time
    for d in all_days:
      for s in all_schdules:
        model.Add(sum(tasks[(n, d, s)] for n in all_tasks) <= 1)

    #C2: One task should not be duplciate on the same day (can modify this to make it configurable) 
    for n in all_tasks:
      for d in all_days:
        model.Add(sum(tasks[(n, d, s)] for s in all_schdules) <= 1)

    #C3: Task should not exceed than it's no of occurance
    for n in all_tasks:
      no_of_occurance = 0
      for d in all_days:
        for s in all_schdules:
          no_of_occurance += tasks[(n, d, s)]

        model.Add(no_of_occurance <= tasks_dict[n]['no_of_days'])

    #C4: Total duration of single day should not exceed than the active hours
    for d in all_days:
      total_duration = 0
      for s in all_schdules:
        for n in all_tasks:
          
          total_duration += tasks[(n, d, s)] * tasks_dict[n]['duration']

      model.Add(total_duration == total_time_per_day)




    solver = cp_model.CpSolver()
    solver.Solve(model)

    for d in all_days:
        print('Day', d)
        for n in all_tasks:
            for s in all_schdules:
                if solver.Value(tasks[(n, d, s)]) == 1:
                        print(tasks_dict[n]['name'], ' duration: ', tasks_dict[n]['duration'], ' at: ', s)
        print()


if __name__ == '__main__':
    main()
