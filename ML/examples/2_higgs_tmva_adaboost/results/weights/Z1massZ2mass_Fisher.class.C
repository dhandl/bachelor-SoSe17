// Class: ReadFisher
// Automatically generated by MethodBase::MakeClass
//

/* configuration options =====================================================

#GEN -*-*-*-*-*-*-*-*-*-*-*- general info -*-*-*-*-*-*-*-*-*-*-*-

Method         : Fisher::Fisher
TMVA Release   : 4.2.1         [262657]
ROOT Release   : 6.08/00       [395264]
Creator        : dhandl
Date           : Tue Apr 25 16:37:21 2017
Host           : Linux lcgapp-slc6-physical1.cern.ch 2.6.32-642.4.2.el6.x86_64 #1 SMP Wed Aug 24 09:19:54 CEST 2016 x86_64 x86_64 x86_64 GNU/Linux
Dir            : /afs/cern.ch/user/d/dhandl/testareas/MyAnaTools/StatisticsSchool2017/tutorials/examples/2_higgs_tmva_adaboost
Training events: 5000
Analysis type  : [Classification]


#OPT -*-*-*-*-*-*-*-*-*-*-*-*- options -*-*-*-*-*-*-*-*-*-*-*-*-

# Set by User:
V: "False" [Verbose output (short form of "VerbosityLevel" below - overrides the latter one)]
VarTransform: "None" [List of variable transformations performed before training, e.g., "D_Background,P_Signal,G,N_AllClasses" for: "Decorrelation, PCA-transformation, Gaussianisation, Normalisation, each for the given class of events ('AllClasses' denotes all events of all classes, if no class indication is given, 'All' is assumed)"]
H: "False" [Print method-specific help message]
# Default:
VerbosityLevel: "Default" [Verbosity level]
CreateMVAPdfs: "False" [Create PDFs for classifier outputs (signal and background)]
IgnoreNegWeightsInTraining: "False" [Events with negative weights are ignored in the training (but are included for testing and performance evaluation)]
Method: "Fisher" [Discrimination method]
##


#VAR -*-*-*-*-*-*-*-*-*-*-*-* variables *-*-*-*-*-*-*-*-*-*-*-*-

NVar 2
Z1mass                        Z1mass                        Z1mass                        Z1mass                                                          'D'    [40.3139724731,117.127799988]
Z2mass                        Z2mass                        Z2mass                        Z2mass                                                          'D'    [12.1137800217,119.685157776]
NSpec 0


============================================================================ */

#include <vector>
#include <cmath>
#include <string>
#include <iostream>

#ifndef IClassifierReader__def
#define IClassifierReader__def

class IClassifierReader {

 public:

   // constructor
   IClassifierReader() : fStatusIsClean( true ) {}
   virtual ~IClassifierReader() {}

   // return classifier response
   virtual double GetMvaValue( const std::vector<double>& inputValues ) const = 0;

   // returns classifier status
   bool IsStatusClean() const { return fStatusIsClean; }

 protected:

   bool fStatusIsClean;
};

#endif

class ReadFisher : public IClassifierReader {

 public:

   // constructor
   ReadFisher( std::vector<std::string>& theInputVars ) 
      : IClassifierReader(),
        fClassName( "ReadFisher" ),
        fNvars( 2 ),
        fIsNormalised( false )
   {      
      // the training input variables
      const char* inputVars[] = { "Z1mass", "Z2mass" };

      // sanity checks
      if (theInputVars.size() <= 0) {
         std::cout << "Problem in class \"" << fClassName << "\": empty input vector" << std::endl;
         fStatusIsClean = false;
      }

      if (theInputVars.size() != fNvars) {
         std::cout << "Problem in class \"" << fClassName << "\": mismatch in number of input values: "
                   << theInputVars.size() << " != " << fNvars << std::endl;
         fStatusIsClean = false;
      }

      // validate input variables
      for (size_t ivar = 0; ivar < theInputVars.size(); ivar++) {
         if (theInputVars[ivar] != inputVars[ivar]) {
            std::cout << "Problem in class \"" << fClassName << "\": mismatch in input variable names" << std::endl
                      << " for variable [" << ivar << "]: " << theInputVars[ivar].c_str() << " != " << inputVars[ivar] << std::endl;
            fStatusIsClean = false;
         }
      }

      // initialize min and max vectors (for normalisation)
      fVmin[0] = 0;
      fVmax[0] = 0;
      fVmin[1] = 0;
      fVmax[1] = 0;

      // initialize input variable types
      fType[0] = 'D';
      fType[1] = 'D';

      // initialize constants
      Initialize();

   }

   // destructor
   virtual ~ReadFisher() {
      Clear(); // method-specific
   }

   // the classifier response
   // "inputValues" is a vector of input values in the same order as the 
   // variables given to the constructor
   double GetMvaValue( const std::vector<double>& inputValues ) const;

 private:

   // method-specific destructor
   void Clear();

   // common member variables
   const char* fClassName;

   const size_t fNvars;
   size_t GetNvar()           const { return fNvars; }
   char   GetType( int ivar ) const { return fType[ivar]; }

   // normalisation of input variables
   const bool fIsNormalised;
   bool IsNormalised() const { return fIsNormalised; }
   double fVmin[2];
   double fVmax[2];
   double NormVariable( double x, double xmin, double xmax ) const {
      // normalise to output range: [-1, 1]
      return 2*(x - xmin)/(xmax - xmin) - 1.0;
   }

   // type of input variable: 'F' or 'I'
   char   fType[2];

   // initialize internal variables
   void Initialize();
   double GetMvaValue__( const std::vector<double>& inputValues ) const;

   // private members (method specific)
   double              fFisher0;
   std::vector<double> fFisherCoefficients;
};

inline void ReadFisher::Initialize() 
{
   fFisher0 = 7.05162158846;
   fFisherCoefficients.push_back( -0.0477030616235 );
   fFisherCoefficients.push_back( -0.0515708088373 );

   // sanity check
   if (fFisherCoefficients.size() != fNvars) {
      std::cout << "Problem in class \"" << fClassName << "\"::Initialize: mismatch in number of input values"
                << fFisherCoefficients.size() << " != " << fNvars << std::endl;
      fStatusIsClean = false;
   }         
}

inline double ReadFisher::GetMvaValue__( const std::vector<double>& inputValues ) const
{
   double retval = fFisher0;
   for (size_t ivar = 0; ivar < fNvars; ivar++) {
      retval += fFisherCoefficients[ivar]*inputValues[ivar];
   }

   return retval;
}

// Clean up
inline void ReadFisher::Clear() 
{
   // clear coefficients
   fFisherCoefficients.clear(); 
}
   inline double ReadFisher::GetMvaValue( const std::vector<double>& inputValues ) const
   {
      // classifier response value
      double retval = 0;

      // classifier response, sanity check first
      if (!IsStatusClean()) {
         std::cout << "Problem in class \"" << fClassName << "\": cannot return classifier response"
                   << " because status is dirty" << std::endl;
         retval = 0;
      }
      else {
         if (IsNormalised()) {
            // normalise variables
            std::vector<double> iV;
            iV.reserve(inputValues.size());
            int ivar = 0;
            for (std::vector<double>::const_iterator varIt = inputValues.begin();
                 varIt != inputValues.end(); varIt++, ivar++) {
               iV.push_back(NormVariable( *varIt, fVmin[ivar], fVmax[ivar] ));
            }
            retval = GetMvaValue__( iV );
         }
         else {
            retval = GetMvaValue__( inputValues );
         }
      }

      return retval;
   }
