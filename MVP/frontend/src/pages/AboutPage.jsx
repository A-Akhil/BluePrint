import { 
  BeakerIcon, 
  AcademicCapIcon, 
  UsersIcon, 
  TrophyIcon,
  GlobeAltIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

const AboutPage = () => {
  return (
    <div className="min-h-screen bg-deep-50 dark:bg-deep-900">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-deep-900 dark:text-white mb-4">
            About DeepSea eDNA Explorer
          </h1>
          <p className="text-xl text-deep-600 dark:text-deep-300 max-w-3xl mx-auto">
            Revolutionizing marine biodiversity research through AI-driven environmental DNA analysis 
            and the groundbreaking ZHNSW algorithm for deep-sea ecosystem discovery.
          </p>
        </div>

        {/* Mission Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          <div className="card p-8">
            <div className="flex items-center mb-4">
              <GlobeAltIcon className="w-8 h-8 text-ocean-600 mr-3" />
              <h2 className="text-2xl font-bold text-deep-900 dark:text-white">Our Mission</h2>
            </div>
            <p className="text-deep-700 dark:text-deep-300 leading-relaxed">
              To democratize marine biodiversity research by providing cutting-edge AI tools that enable 
              researchers, conservationists, and policymakers to understand and protect our ocean's 
              most mysterious and biodiverse deep-sea ecosystems through advanced environmental DNA analysis.
            </p>
          </div>

          <div className="card p-8">
            <div className="flex items-center mb-4">
              <BeakerIcon className="w-8 h-8 text-ocean-600 mr-3" />
              <h2 className="text-2xl font-bold text-deep-900 dark:text-white">Innovation</h2>
            </div>
            <p className="text-deep-700 dark:text-deep-300 leading-relaxed">
              Our proprietary ZHNSW (Zonal Hierarchical Navigable Small World) algorithm represents 
              a paradigm shift in sequence analysis, achieving 47x faster processing while maintaining 
              97.3% accuracy compared to traditional methods, enabling real-time biodiversity assessment.
            </p>
          </div>
        </div>

        {/* Problem Statement */}
        <div className="card p-8 mb-12">
          <div className="flex items-center mb-6">
            <TrophyIcon className="w-8 h-8 text-amber-600 mr-3" />
            <h2 className="text-2xl font-bold text-deep-900 dark:text-white">Smart India Hackathon 2025</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-semibold text-deep-900 dark:text-white mb-3">Problem Statement #25042</h3>
              <p className="text-deep-700 dark:text-deep-300 mb-4">
                "Identifying Taxonomy and Assessing Biodiversity from eDNA Datasets"
              </p>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-deep-600 dark:text-deep-400">Organization:</span>
                  <span className="text-deep-900 dark:text-white">Ministry of Earth Sciences (MoES)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-deep-600 dark:text-deep-400">Department:</span>
                  <span className="text-deep-900 dark:text-white">CMLRE</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-deep-600 dark:text-deep-400">Category:</span>
                  <span className="text-deep-900 dark:text-white">Software</span>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-deep-900 dark:text-white mb-3">Challenge Description</h3>
              <ul className="text-deep-700 dark:text-deep-300 text-sm space-y-2">
                <li>• Deep-sea organisms poorly represented in reference databases</li>
                <li>• Traditional pipelines (QIIME2, DADA2) inadequate for novel taxa</li>
                <li>• Need for AI-driven direct eDNA classification</li>
                <li>• Real-time processing requirements for marine expeditions</li>
                <li>• Integration with existing bioinformatics workflows</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Technical Achievements */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-deep-900 dark:text-white mb-6 text-center">
            Technical Achievements
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <AchievementCard
              icon={ChartBarIcon}
              title="47x Faster Processing"
              description="ZHNSW algorithm achieves sub-20ms query times compared to 847ms traditional methods"
              color="green"
            />
            <AchievementCard
              icon={BeakerIcon}
              title="97.3% Accuracy Maintained"
              description="High accuracy preservation while dramatically reducing computational requirements"
              color="blue"
            />
            <AchievementCard
              icon={GlobeAltIcon}
              title="64 Zone Coverage"
              description="Comprehensive biogeographic zone mapping for Indo-Pacific deep-sea environments"
              color="purple"
            />
          </div>
        </div>

        {/* Team Section */}
        <div className="card p-8 mb-12">
          <div className="flex items-center mb-6">
            <UsersIcon className="w-8 h-8 text-ocean-600 mr-3" />
            <h2 className="text-2xl font-bold text-deep-900 dark:text-white">Development Team</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <TeamMember
              name="Lead Developer"
              role="AI/ML & Frontend Architecture"
              expertise="ZHNSW Algorithm, React.js, Bioinformatics"
            />
            <TeamMember
              name="Marine Biologist"
              role="Domain Expert & Data Validation"
              expertise="Deep-sea Ecology, eDNA Analysis, Taxonomy"
            />
            <TeamMember
              name="Data Scientist"
              role="Algorithm Development"
              expertise="Machine Learning, Sequence Analysis, Statistics"
            />
            <TeamMember
              name="UI/UX Designer"
              role="User Experience & Visualization"
              expertise="Scientific Interfaces, Data Visualization"
            />
          </div>
        </div>

        {/* Technology Stack */}
        <div className="card p-8 mb-12">
          <h2 className="text-2xl font-bold text-deep-900 dark:text-white mb-6">Technology Stack</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-semibold text-deep-900 dark:text-white mb-4">Frontend Technologies</h3>
              <div className="space-y-3">
                <TechItem name="React.js 18" description="Modern component-based UI framework" />
                <TechItem name="Vite" description="Lightning-fast build tool and dev server" />
                <TechItem name="TailwindCSS" description="Utility-first CSS framework for responsive design" />
                <TechItem name="Zustand" description="Lightweight state management solution" />
                <TechItem name="Heroicons" description="Professional icon system" />
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-deep-900 dark:text-white mb-4">Algorithm & Data</h3>
              <div className="space-y-3">
                <TechItem name="ZHNSW Algorithm" description="Proprietary zonal hierarchical search" />
                <TechItem name="Mock Data Simulation" description="256K+ realistic marine sequences" />
                <TechItem name="Confidence Scoring" description="AI-driven taxonomic assignment confidence" />
                <TechItem name="Novelty Detection" description="Machine learning-based species discovery" />
                <TechItem name="Zone Optimization" description="Biogeographic partitioning strategy" />
              </div>
            </div>
          </div>
        </div>

        {/* Impact */}
        <div className="text-center">
          <h2 className="text-2xl font-bold text-deep-900 dark:text-white mb-4">
            Transforming Marine Research
          </h2>
          <p className="text-lg text-deep-600 dark:text-deep-300 max-w-4xl mx-auto">
            Our platform empowers researchers to discover and classify marine biodiversity at unprecedented 
            scale and speed, contributing to ocean conservation efforts and advancing our understanding 
            of Earth's largest and least explored ecosystem.
          </p>
          
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4 max-w-3xl mx-auto">
            <div className="bg-ocean-50 dark:bg-ocean-900/20 p-4 rounded-lg">
              <div className="text-2xl font-bold text-ocean-900 dark:text-ocean-100">256K+</div>
              <div className="text-sm text-ocean-700 dark:text-ocean-300">Marine Sequences Analyzed</div>
            </div>
            <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-900 dark:text-green-100">97.3%</div>
              <div className="text-sm text-green-700 dark:text-green-300">Classification Accuracy</div>
            </div>
            <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-900 dark:text-purple-100">64</div>
              <div className="text-sm text-purple-700 dark:text-purple-300">Deep-sea Zones Covered</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const AchievementCard = ({ icon: Icon, title, description, color }) => {
  const colorClasses = {
    green: 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400',
    blue: 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400',
    purple: 'bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400'
  };

  return (
    <div className="card p-6 text-center">
      <div className={`w-12 h-12 mx-auto mb-4 rounded-lg flex items-center justify-center ${colorClasses[color]}`}>
        <Icon className="w-6 h-6" />
      </div>
      <h3 className="text-lg font-semibold text-deep-900 dark:text-white mb-2">{title}</h3>
      <p className="text-sm text-deep-600 dark:text-deep-300">{description}</p>
    </div>
  );
};

const TeamMember = ({ name, role, expertise }) => {
  return (
    <div className="text-center">
      <div className="w-16 h-16 bg-gradient-to-r from-ocean-500 to-ocean-600 rounded-full mx-auto mb-3 flex items-center justify-center">
        <span className="text-white font-bold text-lg">
          {name.split(' ').map(n => n[0]).join('')}
        </span>
      </div>
      <h3 className="font-semibold text-deep-900 dark:text-white">{name}</h3>
      <p className="text-sm text-ocean-600 dark:text-ocean-400 mb-2">{role}</p>
      <p className="text-xs text-deep-600 dark:text-deep-400">{expertise}</p>
    </div>
  );
};

const TechItem = ({ name, description }) => {
  return (
    <div className="flex items-start">
      <div className="w-2 h-2 bg-ocean-600 rounded-full mt-2 mr-3 flex-shrink-0"></div>
      <div>
        <div className="font-medium text-deep-900 dark:text-white">{name}</div>
        <div className="text-sm text-deep-600 dark:text-deep-300">{description}</div>
      </div>
    </div>
  );
};

export default AboutPage;
