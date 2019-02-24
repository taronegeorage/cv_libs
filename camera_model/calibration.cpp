#include <iostream>
#include <sstream>
#include <time.h>
#include <stdio.h>
#include <string>

#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;


void calibration(string imgs_dir, int num, Size pattern_size, Size square_size, Mat &cameraMatrix, Mat &distCoeffs, vector<Mat> &rvecsMat, vector<Mat> &tvecsMat)
{
    // store the corners
    vector<vector<Point2f> > image_points_seq;
    vector<Point2f> image_points;
    int image_count = 0;
    Size image_size;

    // read crossboard images and find corners on them
    for(int i = 1; i <= num; i++){
        ostringstream oss;
        oss << imgs_dir << i <<".jpg";
        char* filename = &(oss.str())[0];
        Mat img = imread(filename);
        if (i == 1){
            image_size.width = img.cols;
            image_size.height = img.rows;
        }
        /*
        int row = 7;
        int col = 10;
        int n = row * col;
        */
        CvPoint2D32f corners[70];
        
        bool found = findChessboardCorners(img, pattern_size, image_points, CV_CALIB_CB_ADAPTIVE_THRESH | CV_CALIB_CB_NORMALIZE_IMAGE);
        drawChessboardCorners(img, pattern_size, image_points, true);
        if(found == 1){
            cout <<"extract corners successfully in the "<< i <<"th image."<<endl; 
            Mat gray_img;
            cvtColor(img, gray_img, CV_RGB2GRAY);
            cv::cornerSubPix(gray_img, image_points, cv::Size(11, 11), cv::Size(-1, -1), cv::TermCriteria(CV_TERMCRIT_ITER + CV_TERMCRIT_EPS, 20, 0.01));
            image_points_seq.push_back(image_points);
            image_count++;
        }
        else{
            cout <<"The "<< i <<"th image can fail to extract corners."<<endl; 
        }     
        ostringstream name;
        name << "Find and Draw ChessBoard" << i;
        namedWindow(&(name.str())[0], 1 );
        imshow( &(name.str())[0], img );
        cvWaitKey(0); 
        img.release();
        cvDestroyWindow(&(name.str())[0]);
    }

    vector<vector<Point3f> > object_points_seq;
    for (int t = 0;t < image_count;t++)
    {
        vector<Point3f> object_points;
        for (int i = 0;i < pattern_size.height;i++)
        {
            for (int j = 0;j < pattern_size.width;j++)
            {
                Point3f realPoint;
                /* Assume the z values of the crossboard are zeros.  */
                realPoint.x = i*square_size.width;
                realPoint.y = j*square_size.height;
                realPoint.z = 0;
                object_points.push_back(realPoint);
            }
        }
        object_points_seq.push_back(object_points);
    }

    /* Calibrate */
    double err_first = calibrateCamera(object_points_seq, image_points_seq, image_size, cameraMatrix, distCoeffs, rvecsMat, tvecsMat, CV_CALIB_FIX_K3);
    cout << "Reprojection error：" << err_first << " pixels" << endl << endl;
    cout << "Finish" << endl;


    cout << "Evaluation step"<<endl;
    double total_err = 0.0;           
    double err = 0.0;                  // avg error in img
    double totalErr = 0.0;
    double totalPoints = 0.0;
    vector<Point2f> image_points_pro;     // reprojected points

    for (int i = 0;i < image_count;i++)
    {

        projectPoints(object_points_seq[i], rvecsMat[i], tvecsMat[i], cameraMatrix, distCoeffs, image_points_pro);   //通过得到的摄像机内外参数，对角点的空间三维坐标进行重新投影计算

        err = norm(Mat(image_points_seq[i]), Mat(image_points_pro), NORM_L2);

        totalErr += err*err;
        totalPoints += object_points_seq[i].size();

        err /= object_points_seq[i].size();
        total_err += err;
    }
    cout << "sqrt(totalErr / totalPoints): " << sqrt(totalErr / totalPoints) << " pixels" << endl << endl;
    cout << "total_err / image_count：" << total_err / image_count << " pixels" << endl << endl;


    cout << "Final results" << endl;
    Mat rotation_matrix = Mat(3, 3, CV_32FC1, Scalar::all(0)); 
    cout << "Mint: " << endl;
    cout << cameraMatrix << endl << endl;
    cout << "distortion: "<<endl;
    cout << distCoeffs << endl << endl << endl;
    for (int i = 0; i < image_count; i++)
    {
        cout << "The rotation vector for " << i + 1 << "th images：" << endl;
        cout << rvecsMat[i] << endl;

        Rodrigues(rvecsMat[i], rotation_matrix);
        cout << "The rotation matrix for " << i + 1 << "th images：" << endl;
        cout << rotation_matrix << endl;
        cout << "The translation matrix for " << i + 1 << "th images：" << endl;
        cout << tvecsMat[i] << endl << endl;
    }
    cout << endl;
    

}


int main()
{
    string imgs_dir = "./imgs/";                           //images directory
    int num = 15;
    Size board_size = Size(7, 10);                         // row and col
    Size square_size = Size(25, 25);                       // square size

    Mat cameraMatrix = Mat(3, 3, CV_32FC1, Scalar::all(0));        // Intrinsic parameters
    Mat distCoeffs = Mat(1, 5, CV_32FC1, Scalar::all(0));          // Distortion coefficients：k1,k2,p1,p2,k3
    vector<Mat> rvecsMat;                                          // All rotation vectors
    vector<Mat> tvecsMat;                                          // All translation

    calibration(imgs_dir, num, board_size, square_size, cameraMatrix, distCoeffs, rvecsMat, tvecsMat);

    
     
 
    return 0;
}