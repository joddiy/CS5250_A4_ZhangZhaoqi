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
    _process_list = process_list.copy()
    schedule = []
    len_process = len(_process_list)
    ready_queue = [_process_list.pop(0)] # insert the first process
    current_time = 0
    waiting_time = 0
    while len(ready_queue) > 0 or len(_process_list) > 0:
        current_process = None
        if len(ready_queue) != 0: # still task need to be run
            current_process = ready_queue.pop(0) # get a task from the head of queue
            schedule.append((current_time, current_process.id))
            if current_process.burst_time > time_quantum: # run the task for a quantum, then insert to the end of queue
                current_process.burst_time -= time_quantum
                current_time += time_quantum
                process_return_to_list = True
            else: # finish the task
                current_time += current_process.burst_time
                current_process.burst_time = 0
                waiting_time += (current_time - current_process.arrive_time)
        else: # no task anymore
            current_time += time_quantum
        while True: # check whether comes in new task
            if len(_process_list) != 0 and _process_list[0].arrive_time <= current_time: # assuming insert new task happend before insert back old task
                ready_queue.append(_process_list.pop(0))
            else:
                break
        if current_process is not None and current_process.burst_time > 0:
            ready_queue.append(current_process)
    average_waiting_time = waiting_time/float(len_process)
    return schedule, average_waiting_time
        

    return (["to be completed, scheduling process_list on round robin policy with time_quantum"], 0.0)

def SRTF_scheduling(process_list):
    _process_list = process_list.copy()
    schedule = []
    len_process = len(_process_list)
    reamining_queue = [_process_list.pop(0)] # insert the first process
    current_time = 0
    waiting_time = 0
    while len(reamining_queue) > 0 or len(_process_list) > 0:
        if len(reamining_queue) == 0:
            reamining_queue.append(_process_list.pop(0))
        elif len(_process_list) == 0 or current_time + reamining_queue[0].burst_time <= _process_list[0].arrive_time:
            tmp_process = reamining_queue.pop(0)
            schedule.append((current_time, tmp_process.id))
            current_time += tmp_process.burst_time
            waiting_time += (current_time - tmp_process.arrive_time)
        else: ## comes in a new task
            tmp_process = _process_list.pop[0]
            remaining_time = current_time + reamining_queue[0].burst_time - tmp_process.arrive_time
            if remaining_time > tmp_process.burst_time: # need preemptive
                schedule.append((current_time, reamining_queue[0].id))
                current_time = tmp_process.arrive_time
                reamining_queue[0].burst_time = remaining_time
                reamining_queue.insert(0, tmp_process)
            else:
                reamining_queue.append(tmp_process)
                sorted(reamining_queue, key=lambda x: x.burst_time)
    average_waiting_time = waiting_time/float(len_process)
    return schedule, average_waiting_time

def SJF_scheduling(process_list, alpha):
    return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)


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

