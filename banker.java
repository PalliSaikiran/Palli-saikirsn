public interface Bank
{
    
        public void addCustomer(int threadNum, int[] maxDemand);
 
    
        public void getState();
 
   
         
    public boolean requestResources(int threadNum, int[] request);
 
      
        public  void releaseResources(int threadNum, int[] release);
}
public class BankImpl implements Bank
{
    private int n;          
    private int m;          
    private int[] available;    
    private int[][] maximum;    
    private int[][] allocation;     
    private int[][] need;              
 
    
    public BankImpl(int[] resources) {
        
        m = resources.length;
                n = Customer.COUNT;
 
        available = new int[m];
        System.arraycopy(resources,0,available,0,m);
 
                
                maximum = new int[Customer.COUNT][];
                allocation = new int[Customer.COUNT][];
                need = new int[Customer.COUNT][];
    }
       
        public void addCustomer(int threadNum, int[] maxDemand) {
            maximum[threadNum] = new int[m];
            allocation[threadNum] = new int[m];
            need[threadNum] = new int[m];
             
            System.arraycopy(maxDemand, 0, maximum[threadNum], 0, maxDemand.length);
            System.arraycopy(maxDemand, 0, need[threadNum], 0, maxDemand.length);
        }
    }