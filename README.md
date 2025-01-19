# **Beamforming Simulator**

Beamforming is a pivotal technology in modern systems like wireless communications, radar, ultrasound, and biomedical applications. This project presents a **2D Beamforming Simulator** that allows users to explore, customize, and visualize beamforming scenarios in real time. The simulator provides intuitive controls, flexible customization, and clear visualizations for various applications.

---

## **Video Demo**

https://github.com/user-attachments/assets/7af93bb1-0a6b-47ba-b021-24cd3ee387c6

---

## **Overview**

Below is a screenshot showcasing the overall design and interface of the simulator:

![App Design Overview](https://github.com/user-attachments/assets/7ed47a00-2fa8-46cd-a634-4b6f1c3925ce)

---

## **Features**

### **Core Functionality**
- **Beam Steering**: Customize steering angles in real time with visual feedback.  
- **Phased Array Geometry**: Choose between linear and curved arrays, with adjustable curvature parameters.  
- **Constructive/Destructive Interference Mapping**: Visualize the beam profile and interference map in synchronized views.  
- **Multiple Array Units**: Add multiple phased array units, each with adjustable parameters and locations.  

---
## **Equations Used**

The beamforming simulator relies on the following equations for key computations:

### **1. Intensity Map**
The intensity map is computed as:

- **Phase Shift**:

$$
\text{Phase Shift} = -k \cdot (x \cdot \sin(\text{Steering Angle}) + y \cdot \cos(\text{Steering Angle}))
$$


- **Intensity Map**:

$$
\text{Intensity Map} = \left| \sum_{\text{elements}} \exp\left(j \cdot (k \cdot \text{Distances} + \text{Phase Shift})\right) \right|^2
$$

  where:
  
$$
\text{Distance} = \sqrt{(X - x_{\text{element}})^2 + (Y - y_{\text{element}})^2}
$$

- **Normalization**: 

$$
\text{Normalized Intensity} = \frac{\text{Intensity Map}}{\max(\text{Intensity Map})}
$$

---

### **2. Beam Profile (Array Factor)**

The beam profile (or array factor) is given by: 

$$
\text{Array Factor} = \left| \sum_{\text{elements}} \exp\left(j \cdot \left[k \cdot (x \cdot \sin(\theta) + y \cdot \cos(\theta)) + \text{Phase Shift}\right]\right) \right|^2
$$


---

### **3. Array Geometry**

The positions of the array elements depend on the geometry:

- **Linear Array**: 
  
$$
x_i = i \cdot \text{Element Spacing} - \frac{(N-1) \cdot \text{Element Spacing}}{2}, \quad y_i = 0
$$

- **Curved Array**:
  
$$
x_i = R \cdot \cos(\text{Angle}) - R, \quad y_i = R \cdot \sin(\text{Angle})
$$


---


## **Scenarios**

The simulator supports three distinct scenarios, each designed to address specific applications of beamforming:

### **1. 5G Communications**
- **Objective**: Simulate a beamforming scenario where the system focuses on signals originating from a desired steering angle.  
- **Explanation**: In 5G communications, it’s common to target a specific user or signal source while allowing other signals to exist in different angles. The simulator demonstrates how beamforming can isolate the desired signal while maintaining the presence of others. This scenario highlights constructive interference in the target angle and the corresponding destructive patterns elsewhere.  
- **Key Parameters**:
  - Multiple operating frequencies.
  - Adjustable steering angles for signal focus.
  - Visualization of interference patterns.
- **Screenshot**:  
  ![5G Scenario](https://github.com/user-attachments/assets/a2815d1b-5e8a-4c9e-a761-32c3c8f5c06e)

---

### **2. Ultrasound Imaging**
- **Objective**: Model a beamforming scenario where the system produces wide signals covering a specific range in the desired direction.  
- **Explanation**: Ultrasound imaging requires beams that span a range to provide a complete image. In this scenario, the simulator generates wide beams that ensure the entire target area is covered. It also ensures the frequency is optimized for patient safety, avoiding side effects from excessive energy levels.  
- **Key Parameters**:
  - Adjustable beam width to cover a larger range.
  - Frequencies fine-tuned for safe medical use.
  - Synchronized visualization of beam profile and interference map.
- **Screenshot**:  
  ![Ultrasound Scenario](https://github.com/user-attachments/assets/2b36186f-24cc-48aa-b9de-fcfd35ba97e2)

---

### **3. Tumor Ablation**
- **Objective**: Simulate a narrow, focused beam targeting a specific cell or area.  
- **Explanation**: Tumor ablation involves using highly targeted beams to destroy cancerous cells without affecting surrounding healthy tissue. The simulator generates a narrow beam with high precision in the desired steering angle. Like the ultrasound scenario, the operating frequency is chosen carefully to ensure no harmful side effects occur.  
- **Key Parameters**:
  - Narrow beam width for precise targeting.
  - High accuracy to prevent interaction with adjacent cells.
  - Adjustable array curvature for optimal focus.
- **Screenshot**:  
  ![Tumor Ablation Scenario](https://github.com/user-attachments/assets/f3d72381-126e-4902-8aad-f0908179693e)

---

## **How to Run the Project**

1. Clone the repository:
   ```bash
   git clone https://github.com/YassienTawfikk/2D-Beamforming-Simulator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd 2D-Beamforming-Simulator
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python Main.py
   ```

---

## **Team**

This project wouldn’t have been possible without the hard work and collaboration of my amazing team. Huge shout-out to:

- [Nancy Mahmoud](https://github.com/nancymahmoud1)  
- [Madonna Mosaad](https://github.com/madonna-mosaad)  
- [Yassien Tawfik](https://github.com/YassienTawfikk)

---

## **Contact**

For any questions or suggestions, feel free to reach out:

- **Name**: Yassien Tawfik  
- **Email**: [Yassien.m.m.tawfik@gmail.com](mailto:Yassien.m.m.tawfik@gmail.com)
