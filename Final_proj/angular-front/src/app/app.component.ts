import { Component } from '@angular/core';
import {HttpClient, HttpHeaders, HttpResponse} from '@angular/common/http';
import { IResponse } from './IResponse';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'NER';
  textInput: string;
  loading = false;
  plot: any;
  imgShow = false;
  response: IResponse[];
  constructor(
    private http: HttpClient,
  ) {
  }

  sendText(text: string) {
    const request = {
      data: text
    };
    this.loading = true;
    this.http.post('http://localhost:5000/predict_str', request).subscribe((response: IResponse[]) => {
      this.response = response;
    },
      null,
      () => this.loading = false);
  }

  sendFile(event): void {
    const fileList: FileList = event.target.files;
    if (fileList.length > 0) {
      const file = fileList[0];
      const formData = new FormData();
      formData.append('file', file, file.name);
      this.loading = true;
      this.http.post( 'http://localhost:5000/predict_file', formData,
        {headers: new HttpHeaders({enctype: 'multipart/form-data', Accept: 'application/json'}),
        responseType: 'blob'})
        .subscribe((response: Blob) => {
             this.createImageFromBlob(response);
        },
          null,
          () => {
          this.loading = false;
          this.imgShow = true;
          });
    }
  }

  createImageFromBlob(image: Blob) {
    const reader = new FileReader();
    reader.addEventListener('load', () => {
      this.plot = reader.result;
    }, false);

    if (image) {
      reader.readAsDataURL(image);
    }
  }

  hideImg() {
    this.imgShow = false;
  }
}
