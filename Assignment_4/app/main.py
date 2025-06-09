from mpi4py import MPI
from mpi_master import run_master
from mpi_worker import run_worker

def main():
    """
    Entry point for the MPI-based prediction service.

    This function initializes the MPI environment, determines the rank and size of the process group,
    and delegates execution to either the master or worker logic depending on the rank.
    - Rank 0 acts as the master node and calls run_master().
    - All other ranks act as worker nodes and call run_worker().
    """
    print("=== Starting MPI Prediction Service ===")
    comm = MPI.COMM_WORLD            # Get the global communicator
    rank = comm.Get_rank()           # This process's rank in the communicator
    size = comm.Get_size()           # Total number of processes
    if rank == 0:
        # Master process runs coordination logic
        run_master(comm, size)
    else:
        # Worker processes run prediction tasks
        run_worker(comm, rank)

if __name__ == "__main__":
    # Only run main() if this file is executed as the main module
    main()
