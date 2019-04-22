'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys
import copy

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time, process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum):
    _process_list = copy.deepcopy(process_list)
    schedule = []
    ready_queue = []
    last_execute_end = dict()
    current_time = 0
    waiting_time = 0
    while len(ready_queue) > 0 or len(_process_list) > 0:
        if len(ready_queue) != 0: # still task need to be run
            tmp_process = ready_queue.pop(0) # get a task from the head of queue
            waiting_time += (current_time - last_execute_end[tmp_process.id])
            schedule.append((current_time, tmp_process.id))
            # check whether comes in new task
            while len(_process_list) > 0 and current_time + time_quantum >= _process_list[0].arrive_time:
                come_processs = _process_list.pop(0)
                ready_queue.append(come_processs)
                last_execute_end[come_processs.id] = come_processs.arrive_time
            if tmp_process.burst_time > time_quantum: # run the task for a quantum, then insert to the end of queue
                current_time += time_quantum
                last_execute_end[tmp_process.id] = current_time
                tmp_process.burst_time -= time_quantum
                ready_queue.append(tmp_process)
            else: # finish the task
                current_time += tmp_process.burst_time
                tmp_process.burst_time = 0
                del last_execute_end[tmp_process.id]
        elif len(_process_list) != 0: # no task anymore, request a new process
            come_processs = _process_list.pop(0)
            ready_queue.append(come_processs)
            current_time = come_processs.arrive_time
            last_execute_end[come_processs.id] = come_processs.arrive_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

def SRTF_scheduling(process_list):  
    _process_list = copy.deepcopy(process_list)
    schedule = []
    reamining_queue = []
    last_execute_end = dict()
    current_time = 0
    waiting_time = 0
    while len(reamining_queue) > 0 or len(_process_list) > 0:
        if len(reamining_queue) != 0:
            tmp_process = reamining_queue.pop(0) # get a task from the head of queue
            if len(schedule) == 0 or schedule[-1][1] != tmp_process.id:
                waiting_time += (current_time - last_execute_end[tmp_process.id])
                schedule.append((current_time, tmp_process.id))
            # check whether comes in new task
            if len(_process_list) > 0 and current_time + tmp_process.burst_time > _process_list[0].arrive_time:
                tmp_process.burst_time = current_time + tmp_process.burst_time - _process_list[0].arrive_time
                reamining_queue.append(tmp_process)
                come_processs = _process_list.pop(0)
                last_execute_end[tmp_process.id] = come_processs.arrive_time
                current_time = come_processs.arrive_time
                reamining_queue.append(come_processs)
                last_execute_end[come_processs.id] = come_processs.arrive_time
                reamining_queue = sorted(reamining_queue, key=lambda x: x.burst_time * 1e5 + x.arrive_time) # sort remaining queue
            else: # finish the task
                current_time += tmp_process.burst_time
                tmp_process.burst_time = 0
                del last_execute_end[tmp_process.id]
        elif len(_process_list) != 0:
            come_processs = _process_list.pop(0)
            reamining_queue.append(come_processs)
            current_time = come_processs.arrive_time
            last_execute_end[come_processs.id] = come_processs.arrive_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

def SJF_scheduling(process_list, alpha):
    _process_list = copy.deepcopy(process_list)
    schedule = []
    guess_value = dict((process.id, 5) for process in process_list) # init guess = 5
    last_execute_end = dict((process.id, 0) for process in process_list) # init last exectue end time = 0
    ready_queue = []
    current_time = 0
    waiting_time = 0
    while len(ready_queue) > 0 or len(_process_list) > 0:
        if len(ready_queue) != 0: # still task need to be run
            min_id = 0
            min_guess = 1e5
            for id, process in enumerate(ready_queue):
                if guess_value[process.id] < min_guess:
                    min_guess = guess_value[process.id]
                    min_id = id
            tmp_process = ready_queue.pop(min_id) # get a task which has smallest guess value 
            waiting_time += (current_time - last_execute_end[tmp_process.id])
            schedule.append((current_time, tmp_process.id))
            # check whether comes in new task
            while len(_process_list) > 0 and current_time + tmp_process.burst_time >= _process_list[0].arrive_time:
                come_processs = _process_list.pop(0)
                ready_queue.append(come_processs)
                last_execute_end[come_processs.id] = come_processs.arrive_time
            # finish this task and update guess value
            current_time += tmp_process.burst_time
            last_execute_end[tmp_process.id] = current_time
            guess_value[tmp_process.id] = alpha * tmp_process.burst_time + (1 - alpha) * guess_value[tmp_process.id]
            tmp_process.burst_time = 0
            del last_execute_end[tmp_process.id]
        elif len(_process_list) != 0: # no task anymore, request a new process
            come_processs = _process_list.pop(0)
            ready_queue.append(come_processs)
            current_time = come_processs.arrive_time
            last_execute_end[come_processs.id] = come_processs.arrive_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])

